from datetime import date
import os

from reportlab.pdfgen import canvas

from cali.lib.db import get_db
from cali.lib.client import Client
#from cali.lib.user import get_single_user
from cali.lib.credit import Credit

class Sale:
    """ A simple sale class """

    def __init__(self, iterable):
        self.id = self.get_id()
        self.userId = iterable['user_id']
        self.clientId = iterable['client_id']
        self.user =  get_single_user(self.userId)['username']
        self.client = Client.get_single_client(self.clientId)['name']
        self.total = float(iterable['total'])
        self.discount = iterable['Discount']
        self.totalArticles = iterable['total_articles']
        self.recivedCash = self.get_recived_cash(iterable) 
        self.payMethodId = int(iterable['PayMethodId'])
        self.payMethod = self.get_pay_method()
        self.branchId = iterable['branch_id']
        self.change = self.get_change()
        self.date = self.get_date()
        self.operationType = iterable['operation_type']
        self.creditTime = iterable['creditTime']

    def create_sale(self, cartItems):
        if self.operationType == 'credit':
            self.create_items_database(cartItems)
            return "INSERT INTO credit(user_id, branch_id, client_id, total, payed, pay_method_id, date, credit_time ) " \
            f"VALUES( {self.userId},{self.branchId}, {self.clientId}, {self.total}, {self.recivedCash}, {self.payMethodId}, '{self.date}', {self.creditTime})"
        else:
            return "INSERT INTO sale(user_id, client_id, total, pay_method_id, date) " \
            f"VALUES( {self.userId}, {self.clientId}, {self.total}, {self.payMethodId}, '{self.date}')"

    def create_items_database(self, cartItems):
        db = get_db()
        tableQuery = self.get_items_database_query(cartItems)
        itemsQuery = self.get_items_query(cartItems)
        try:
            db.execute(tableQuery)
        except: 
            db.execute(f'DROP TABLE credit_{self.id}_items')
            db.execute(tableQuery)
        db.execute(itemsQuery)
        db.commit
        return

    def get_items_database_query(self, cartItems):
        creditId = Credit.get_id()
        tableQuery = f'CREATE TABLE credit_{self.id}_items('
        for count, item in enumerate(cartItems):
            tableQuery += f'item_{count}_sku TEXT, ' 
        tableQuery = tableQuery[:-2]
        tableQuery += ')'
        return tableQuery

    def get_items_query(self, cartItems):
        itemsQuery = f'INSERT INTO credit_{self.id}_items VALUES ('
        for item in cartItems:
            itemsQuery += f'{item["SKU"]}, '
        itemsQuery = itemsQuery[:-2]
        itemsQuery += ')'
        return itemsQuery

    def get_change(self):
        try:
            return float(self.recivedCash) - float(self.total)
        except ValueError:
            return 0

    def get_recived_cash(self, iterable):
        if iterable['recivedCash'] == '':
            return 0
        else:
            return float(iterable['recivedCash'])

    def get_id(self):
        db = get_db()
        sale_id = db.execute(f"SELECT id FROM sale" ).fetchall()
        if sale_id == None:
            sale_id = 1
        return len(sale_id) + 1

    def get_date(self):
        today = date.today()
        return  str(today.strftime('%d/%m/%Y'))

    def format_date(date):
        day = date[-2:]
        month = date[-5:-3]
        year = date[:4]
        date = f'{day}/{month}/{year}'
        return date

    def get_pay_method(self):
        if self.payMethodId == 0:
            return 'Cash'
        else:
            return 'Credit Card'

    def apply_discount(self):
        total = float(self.total)
        discount = int(self.discount)
        self.total = total - (total * discount / 100) 
        self.change = self.get_change()
        return

    def client_has_discount(self):
        db = get_db()
        client = db.execute(f'SELECT * FROM client WHERE id={self.clientId}').fetchone()
        if client['has_credit']:
            return True
        else:
            return False


    def get_all_sales():
        db = get_db()
        sales = db.execute("""
            SELECT * FROM sale
            JOIN user on sale.user_id = user.id
            JOIN client on sale.client_id = client.id
            JOIN pay_method on sale.pay_method_id = pay_method.id
            """
        ).fetchall()
        filtered_sale = False
        return sales, filtered_sale

    def get_sales_information(salesList, filtered_sale):
        saleInformation = {}
        saleInformation['date'] = Sale.get_sales_date(salesList, filtered_sale)
        saleInformation['total sales'] = Sale.get_total_sales(salesList)
        saleInformation['total'] = Sale.get_sales_total(salesList)
        saleInformation['cash sales'] = Sale.get_cash_sales(salesList)
        saleInformation['total cash sales'] = Sale.get_cash_sales_total(salesList)
        saleInformation['credit card sales'] = Sale.get_credit_card_sales(salesList)
        saleInformation['total credit card sales'] = Sale.get_total_credit_card_sales(salesList)

        return saleInformation

    def get_sales_date(salesList, filtered_sale):
        if filtered_sale:
            try:
                return salesList[0]['date']
            except IndexError:
                return '-'
        else:
            return '-'

    def get_total_sales(salesList):
        return len(salesList)

    def get_sales_total(salesList):
        total = 0
        for sale in salesList:
           total += sale['total']
        return total

    def filter_sale_pay_method(salesList, payMethodId):
        filteredSales = []
        for sale in salesList:
            if sale['pay_method_id'] == payMethodId:
                filteredSales.append(sale)
        return filteredSales

    def get_cash_sales(salesList):
        payMethodId = 0
        cashSales = Sale.filter_sale_pay_method(salesList, payMethodId)
        return len(cashSales)

    def get_cash_sales_total(salesList):
        payMethodId = 0
        cashSales = Sale.filter_sale_pay_method(salesList, payMethodId)
        total = Sale.get_sales_total(cashSales)
        return total

    def get_credit_card_sales(salesList):
        payMethodId = 1
        cardSales = Sale.filter_sale_pay_method(salesList, payMethodId)
        return len(cardSales)

    def get_total_credit_card_sales(salesList):
        payMethodId = 1
        cardSales = Sale.filter_sale_pay_method(salesList, payMethodId)
        total = Sale.get_sales_total(cardSales)
        return total

    def cash_is_enough(self):
        if self.recivedCash < self.total:
            return False
        else:
            return True

    def get_filtered_sales(form):
        db = get_db()
        search_date = form['date']
        search_date = Sale.format_date(search_date)

        for key, value in form.items():
            if value is '':
                continue

            if key =='id':
                sales = db.execute('SELECT * FROM sale '
                                   'JOIN user on sale.user_id = user.id '
                                   'JOIN client on sale.client_id = client.id '
                                   'JOIN pay_method on sale.pay_method_id = pay_method.id '
                                   f'WHERE {key}={value}'
                    ).fetchall()
                filtered_sale = True
                return sales, filtered_sale

            elif key =='date':
                sales = db.execute('SELECT * FROM sale '
                                   'JOIN user on sale.user_id = user.id '
                                   'JOIN client on sale.client_id = client.id '
                                   'JOIN pay_method on sale.pay_method_id = pay_method.id '
                                   f'WHERE {key}="{search_date}"'
                    ).fetchall()
                filtered_sale = True
                return sales, filtered_sale

        else:
            sales = db.execute(f'SELECT * FROM sale '
                                'JOIN user on sale.user_id = user.id '
                                'JOIN client on sale.client_id = client.id '
                                'JOIN pay_method on sale.pay_method_id = pay_method.id '
                               ).fetchall()
            filtered_sale = False
            return sales, filtered_sale

    def print_sale_ticket(self, cart_items):
        self.save_txt_ticket(cart_items)
        os.system(f'cat cali/static/tickets/ticket-{self.id}.txt >> /dev/usb/lp0')
        return

    def print_sale_ticket_by_id(id):
        os.system(f'cat cali/static/tickets/ticket-{id}.txt >> /dev/usb/lp0')
        return

    def print_report():
        os.system(f'cat cali/static/reports/sale_report.txt >> /dev/usb/lp0')
        return

    def save_txt_ticket(self, cart_items):
        with open(f'cali/static/tickets/ticket-{self.id}.txt', 'w+') as ticket:
            ticket.write('\n\n     Cali Boutique\n')
            ticket.write('Ave. de la Cantera 9119. \n')
            ticket.write('Plaza Poniente 2do piso. \n')
            ticket.write('(614)184-1424 \n')
            ticket.write(f'Vendedor: {self.user} \n' )
            ticket.write(f'Cliente: {self.client} \n' )
            ticket.write(f'Fecha: {self.date} \n' )
            ticket.write(f'Folio: {self.id} \n' )
            ticket.write('------------------------- \n' )
            for count, item in enumerate(cart_items):
                ticket.write(f'{item["name"]} ' )
                ticket.write(f'{item["price"]} \n' )

            ticket.write('------------------------- \n' )

            ticket.write(f'Total: {self.total} \n' )
            ticket.write(f'Efectivo: {self.recivedCash} \n' )
            ticket.write(f'Cambio: {self.change} \n' )

            ticket.write('------------------------- \n' )
            ticket.write('Gracias por su compra \n')
            ticket.write('Cambios Unicamente 7 dias\ndespues de la compra \n')
            ticket.write('No Reembolsos \n\n\n\n')

            return

    def create_sale_ticket(self, cart_items):
        pageHeight = (len(cart_items) * 10) + 250
        c = canvas.Canvas(f'cali/static/tickets/ticket-{self.id}.pdf', pagesize=(200, pageHeight), bottomup=0)
        c.translate(100, 20)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(0, 0, 'Cali Boutique')
        c.drawCentredString(0, 10, 'Ave. de la Cantera 9119')
        c.drawCentredString(0, 20, 'Plaza Poniente 2do piso.')
        c.drawCentredString(0, 30, '(614)184-1424')

        c.translate(-80, 50)
        c.drawString(0, 10, f'Vendedor: {self.user}' )
        c.drawString(0, 20, f'Cliente: {self.client}' )
        c.drawString(0, 30, f'Fecha: {self.date}' )

        c.translate(80, 40)
        c.drawCentredString(0, 10, f'Folio: {self.id}' )
        c.drawCentredString(0, 20, '------------------------------------------------------------' )

        c.translate(-80, 30)
        for count, item in enumerate(cart_items):
            c.drawString(0, 0, f'{item["id"]}' )
            c.drawString(10, 0, f'{item["name"]}' )
            c.drawString(130, 0, f'{item["price"]}' )
            c.translate(0, 10)

        c.translate(80, 0)
        c.drawCentredString(0, 0, '------------------------------------------------------------' )

        c.translate(-80, 10)
        c.drawString(0, 10, f'Total: {self.total}' )
        c.drawString(0, 20, f'Efectivo: {self.recivedCash}' )
        c.drawString(0, 30, f'Cambio: {self.change}' )

        c.translate(80, 40)
        c.drawCentredString(0, 0, '------------------------------------------------------------' )

        c.translate(-80, 10)
        c.drawString(0, 0, 'gracias por su compra')

        c.showPage()
        c.save()

        return

    def create_txt_report(salesList, salesInformation):
        with open(f'cali/static/reports/sale_report.txt', 'w+') as ticket:
            ticket.write('\n\n     Cali Boutique \n')
            ticket.write('Ave. de la Cantera 9119 \n')
            ticket.write('Plaza Poniente 2do piso. \n')
            ticket.write('(614)184-1424 \n')
            ticket.write('Reporte de Ventas \n')
            ticket.write('------------------------- \n' )

            ticket.write(f'Fecha: {salesInformation["date"]} \n' )
            ticket.write(f'Ventas Totales: {salesInformation["total sales"]} \n' )
            ticket.write(f'Ingreso Total: {salesInformation["total"]} \n' )
            ticket.write(f'Ventas en Efectivo: {salesInformation["cash sales"]} \n' )
            ticket.write(f'Total Ventas En Efectivo: {salesInformation["total cash sales"]} \n' )
            ticket.write(f'Ventas Con Tarjeta: {salesInformation["credit card sales"]} \n' )
            ticket.write(f'Total Ventas Con Tarjeta: {salesInformation["total credit card sales"]} \n' )

            ticket.write('------------------------- \n' )
            ticket.write('Ventas \n' )
            ticket.write('Id|Usuario|Cliente|Fecha|Total \n' )


            for sale in salesList:
                user = get_single_user(sale['user_id'])
                client = Client.get_single_client(sale['client_id'])
                ticket.write(f'{sale["id"]}|{user["username"]}|{client["name"]}|{sale["date"]}|{sale["total"]} \n')

            ticket.write('\n\n\n\n')
            return


    def create_report(salesList, salesInformation):
        pageHeight = (len(salesList) * 10) + 250
        pageWidth = 200
        padding = 20

        c = canvas.Canvas(f'cali/static/reports/sale_report.pdf', pagesize=(pageWidth, pageHeight), bottomup=0)

        c.translate(pageWidth/2, 20)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(0, 0, 'Cali Boutique')
        c.drawCentredString(0, 10, 'Ave. de la Cantera 9119')
        c.drawCentredString(0, 20, 'Plaza Poniente 2do piso.')
        c.drawCentredString(0, 30, '(614)184-1424')
        c.translate(0, 50)

        c.drawCentredString(0, 0, 'Reporte de Ventas')
        c.drawCentredString(0, 10, '------------------------------------------------------------' )

        c.translate(padding-pageWidth/2, 20)
        c.drawString(0, 0, f'Fecha: {salesInformation["date"]}' )
        c.drawString(0, 10, f'Ventas Totales: {salesInformation["total sales"]}' )
        c.drawString(0, 20, f'Ingreso Total: {salesInformation["total"]}' )
        c.drawString(0, 30, f'Ventas en Efectivo: {salesInformation["cash sales"]}' )
        c.drawString(0, 40, f'Total Ventas En Efectivo: {salesInformation["total cash sales"]}' )
        c.drawString(0, 50, f'Ventas Con Tarjeta: {salesInformation["credit card sales"]}' )
        c.drawString(0, 60, f'Total Ventas Con Tarjeta: {salesInformation["total credit card sales"]}' )

        c.translate(-padding+pageWidth/2, 80)
        c.drawCentredString(0, 0, 'Ventas')
        c.drawCentredString(0, 10, '------------------------------------------------------------' )

        c.translate(+padding-pageWidth/2, 20)
        c.drawString(0, 0, 'Id')
        c.drawString(10, 0, f'| Usuario' )
        c.drawString(50, 0, f'| Cliente' )
        c.drawString(90, 0, f'| Fecha' )
        c.drawString(140, 0, f'|  Total' )

        for sale in salesList:
            user = get_single_user(sale['user_id'])
            client = Client.get_single_client(sale['client_id'])

            c.translate(0, 10)
            c.drawString(0, 0, f'{sale["id"]}' )
            c.drawString(10, 0, f'| {user["username"]} ' )
            c.drawString(50, 0, f'| {client["name"]}' )
            c.drawString(90, 0, f'| {sale["date"]}' )
            c.drawString(140, 0, f'| ${sale["total"]}' )

        c.translate(-padding+pageWidth/2, 0)
        c.drawCentredString(0, 10, '------------------------------------------------------------' )
        c.showPage()
        c.save()
        return

import os
from datetime import date
from flask import flash

from reportlab.pdfgen import canvas

from cali.lib.db import get_db
from cali.lib.client import Client
from cali.lib.credit import Credit
from cali.lib.alert import Alert
from cali.lib.user import User
from cali.lib.cart import ShoppingCart

class Sale:
    """ A simple sale class """

    def __init__(self, iterable):
        self.userId = iterable['user_id']
        self.clientId = iterable['client_id']
        self.discount = iterable['Discount']
        self.totalArticles = iterable['total_articles']
        self.operationType = iterable['operation_type']
        self.creditTime = iterable['creditTime']

        self.total = Sale._get_total(iterable)
        self.branchId = Sale._get_branch_id(iterable)
        self.recivedCash = Sale._get_recived_cash(iterable)
        self.payMethodId = Sale._get_pay_method_id(iterable)

        self.id = self._get_id()
        self.date = self._get_date()
        self.payMethod = self._get_pay_method()
        self.change = self._get_change()

        self.user =  User.get_username_by_id(self.userId)
        self.client = Client.get_name_by_id(self.clientId)

    def _get_branch_id(iterable):
        return int(iterable['branch_id'])

    def _get_total(iterable):
        return float(iterable['total'])

    def _get_pay_method_id(iterable):
        return int(iterable['PayMethodId'])

    def _get_recived_cash(iterable):
        if iterable['recivedCash'] == '':
            return 0
        else:
            return float(iterable['recivedCash'])

    def _get_pay_method(self):
        if self.payMethodId == 0:
            return 'Cash'
        else:
            return 'Credit Card'

    def _get_date(self):
        today = date.today()
        return  str(today.strftime('%d/%m/%Y'))

    def _get_change(self):
        if self.payMethod == 'Cash':
            return float(self.recivedCash) - float(self.total)
        else:
            return 0

    def _get_id(self):
        db = get_db()
        sale_id = db.execute(f"SELECT id FROM sale" ).fetchall()
        if sale_id == None:
            sale_id = 1
        return len(sale_id) + 1

    def _client_has_discount(self):
        db = get_db()
        client = db.execute(f'SELECT * FROM client WHERE id={self.clientId}').fetchone()
        return client['has_credit']

    def _cash_is_enough(self):
        return self.recivedCash >= self.total

    def _is_empty_sale(self):
        return self.total == 0

    def _get_items_query(self, cartItems):
        itemsQuery = f'INSERT INTO credit_{self.id}_items VALUES ('
        for item in cartItems:
            itemsQuery += f'{item["SKU"]}, '
        itemsQuery = itemsQuery[:-2]
        itemsQuery += ')'
        return itemsQuery

    def _get_items_database_query(self, cartItems):
        creditId = Credit.get_id()
        tableQuery = f'CREATE TABLE credit_{self.id}_items('
        for count, item in enumerate(cartItems):
            tableQuery += f'item_{count}_sku TEXT, '
        tableQuery = tableQuery[:-2]
        tableQuery += ')'
        return tableQuery

    def _create_credit_database(self, cartItems):
        db = get_db()
        tableQuery = self._get_items_database_query(cartItems)
        itemsQuery = self._get_items_query(cartItems)
        try:
            db.execute(tableQuery)
        except:
            db.execute(f'DROP TABLE credit_{self.id}_items')
            db.execute(tableQuery)
        db.execute(itemsQuery)
        db.commit()
        return

    def _format_date(date):
        day = date[-2:]
        month = date[-5:-3]
        year = date[:4]
        date = f'{day}/{month}/{year}'
        return date

    def _get_sales_date(salesList, filtered_sale):
        if filtered_sale and len(salesList) != 0 :
            return salesList[0]['date']
        else:
            return '-'

    def _get_total_sales(salesList):
        return len(salesList)

    def _get_sales_total(salesList):
        total = 0
        for sale in salesList:
           total += sale['total']
        return total

    def _filter_sales_by_pay_method(salesList, payMethodId):
        filteredSales = []
        for sale in salesList:
            if sale['pay_method_id'] == payMethodId:
                filteredSales.append(sale)
        return filteredSales

    def _get_cash_sales(salesList):
        payMethodId = 0
        cashSales = Sale._filter_sales_by_pay_method(salesList, payMethodId)
        return len(cashSales)

    def _get_cash_sales_total(salesList):
        payMethodId = 0
        cashSales = Sale._filter_sales_by_pay_method(salesList, payMethodId)
        total = Sale._get_sales_total(cashSales)
        return total

    def _get_credit_card_sales(salesList):
        payMethodId = 1
        cardSales = Sale._filter_sales_by_pay_method(salesList, payMethodId)
        return len(cardSales)

    def _get_total_credit_card_sales(salesList):
        payMethodId = 1
        cardSales = Sale._filter_sales_by_pay_method(salesList, payMethodId)
        total = Sale._get_sales_total(cardSales)
        return total

    def is_valid(self, branchId):
        cart = ShoppingCart()
        if self.operationType == 'credit' and not self._client_has_discount():
            Alert.raise_danger_alert("Client has no Discount")
            return False
        elif self._is_empty_sale():
            Alert.raise_danger_alert('Empty Sale')
            return False
        elif self.payMethod == 'Cash' and not self._cash_is_enough():
            Alert.raise_danger_alert('Cash is Not Enought')
            return False
        elif not cart.there_is_enought_stock(branchId):
            Alert.raise_danger_alert('Not Enought Stock')
            return False
        else:
            return True

    def create_sale(self, cartItems, branchId):
        db = get_db()
        if self.operationType == 'credit':
            self._create_credit_database(cartItems)
            data = (self.userId, branchId, self.clientId,
                    self.total, self.payMethodId, self.recivedCash,
                    self.date, self.creditTime)
            query = """
                INSERT INTO credit(user_id, branch_id, client_id,  total, pay_method_id, payed, date, credit_time )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """
        else:
            data = (self.userId, branchId, self.clientId,
                    self.total, self.payMethodId, self.date)
            query = """
                INSERT INTO  sale(user_id, branch_id, client_id,  total, pay_method_id, date)
                VALUES(?, ?, ?, ?, ?, ? )
                """

        db.execute(query, data)
        db.commit()
        return

    def get_filtered_sales(form):
        db = get_db()
        search_date = form['date']
        if search_date:
            search_date = Sale._format_date(search_date)
            data = (search_date,)
            query = """
                    SELECT * FROM sale
                    JOIN user on sale.user_id = user.id
                    JOIN client on sale.client_id = client.id
                    JOIN pay_method on sale.pay_method_id = pay_method.id
                    WHERE date = ?
                """
            sales = db.execute(query, data).fetchall()
            filtered_sale = True
            return sales, filtered_sale

        for key, value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM sale '\
                        'JOIN user on sale.user_id = user.id '\
                        'JOIN client on sale.client_id = client.id '\
                        'JOIN pay_method on sale.pay_method_id = pay_method.id '\
                        f'WHERE sale.{key} = ?'
                sales = db.execute(query, data).fetchall()
                filtered_sale = True
                return sales, filtered_sale


            else:
                sales, filtered_sale = Sale.get_all_sales()
        return sales, filtered_sale

    def get_all_sales():
        db = get_db()
        query = """ SELECT * FROM sale"""
        sales = db.execute(query).fetchall()
        filtered_sale = False
        return sales, filtered_sale

    def create_sales_reports(sales, salesInformation):
        if salesInformation['date'] is not '-':
            Sale.create_report(sales, salesInformation)
            Sale.create_txt_report(sales, salesInformation)
        return

    def apply_discount(self):
        total = float(self.total)
        discount = int(self.discount)
        self.total = total - (total * discount / 100)
        self.change = self.get_change()
        return

    def get_sales_information(salesList, filtered_sale):
        saleInformation = {}
        saleInformation['date'] = Sale._get_sales_date(salesList, filtered_sale)
        saleInformation['total sales'] = Sale._get_total_sales(salesList)
        saleInformation['total'] = Sale._get_sales_total(salesList)
        saleInformation['cash sales'] = Sale._get_cash_sales(salesList)
        saleInformation['total cash sales'] = Sale._get_cash_sales_total(salesList)
        saleInformation['credit card sales'] = Sale._get_credit_card_sales(salesList)
        saleInformation['total credit card sales'] = Sale._get_total_credit_card_sales(salesList)
        return saleInformation

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

    def save_sale_ticket(self, cart_items):
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
                user = User.get_user_by_id(sale['user_id'])
                client = Client.get_client_by_id(sale['client_id'])
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
            user = User.get_user_by_id(sale['user_id'])
            client = Client.get_client_by_id(sale['client_id'])

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

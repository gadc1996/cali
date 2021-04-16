from datetime import date

from reportlab.pdfgen import canvas

from cali.lib.db import get_db
from cali.lib.client import get_single_client
from cali.lib.user import get_single_user

class Sale:
    """ A simple sale class """

    def __init__(self, iterable):
        self.id = self.get_id()
        self.userId = iterable['user_id']
        self.clientId = iterable['client_id']
        self.user =  get_single_user(self.userId)['username']
        self.client = get_single_client(self.clientId)['name']
        self.total = iterable['total']
        self.totalArticles = iterable['total_articles']
        self.recivedCash = iterable['recivedCash']
        self.payMethodId = int(iterable['PayMethodId'])
        self.payMethod = self.get_pay_method()
        self.branchId = iterable['branch_id']
        self.change = self.get_change()
        self.date = self.get_date()

    def create_sale(self):
        return "INSERT INTO sale(user_id, client_id, total, pay_method_id, date) " \
        f"VALUES( {self.userId}, {self.clientId}, {self.total}, {self.payMethodId}, '{self.date}')"

    def get_change(self):
        try:
            return float(self.recivedCash) - float(self.total)
        except ValueError:
            return 0

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

    def get_all_sales():
        db = get_db()
        sales = db.execute("""
            SELECT * FROM sale
            """
        ).fetchall()
        return sales

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
                sales = db.execute(f'SELECT * FROM sale WHERE {key}={value}'
                    ).fetchall()
                return sales

            elif key =='date':
                sales = db.execute(f'SELECT * FROM sale WHERE {key}="{value}"'
                    ).fetchall()
                return sales

            else:
                sales = db.execute(f'SELECT * FROM sale').fetchall()
                return sales

    def create_sale_ticket(self):
        c = canvas.Canvas(f'ticket-{self.id}.pdf', pagesize=(200, 250), bottomup=0)
        c.translate(100, 20)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(0, 0, 'Creaciones "KENDRA"')
        c.drawCentredString(0, 10, 'ALEJANDRINA TORRES RASCON')
        c.drawCentredString(0, 20, 'TORA-580520-538')
        c.drawCentredString(0, 30, 'CALLE 5 DE MAYO NO. 6 COL. CENTRO')
        c.drawCentredString(0, 40, '(652)57-20053')

        c.translate(-80, 50)
        c.drawString(0, 10, f'Vendedor: {self.user}' )
        c.drawString(0, 20, f'Cliente: {self.client}' )
        c.drawString(0, 30, f'Fecha: {self.date}' )

        c.translate(80, 40)
        c.drawCentredString(0, 10, f'Folio: {self.id}' )
        c.drawCentredString(0, 20, '------------------------------------------------------------' )

        c.translate(-80, 30)
        c.drawString(0, 0, '1' )
        c.drawString(10, 0, 'Collar Zebra' )
        c.drawString(130, 0, '$240' )

        c.translate(80, 10)
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
#    def _is_valid(self, field, fieldName):
#        if field is none:
#            raise valueerror(f"{fieldName} Required, value: {field}")
#
#        return field
#
#    def update_sale(self, id):
#        return 'update sale '\
#            f'set name="{self.name}", '\
#            f'contact_phone="{self.contactPhone}", '\
#            f'has_credit={self.hasCredit} '\
#            f'where id={id} '
#
#    def delete_sale(self, id):
#        return f'DELETE FROM sale WHERE id={id}'
#
#def get_single_sale(id):
#    db = get_db()
#    sale = db.execute(f'SELECT name, contact_phone, has_credit FROM sale WHERE id={id}').fetchone()
#    return sale
#

#def get_filtered_sales(form):
#    db = get_db()
#    for key,value in form.items():
#        if value is '':
#            continue
#
#        if key =='id':
#            sales = db.execute(f'SELECT * FROM sale WHERE {key}={value}'
#                ).fetchall()
#            return sales
#
#        else:
#            sales = db.execute(f'SELECT * FROM sale WHERE {key}="{value}"'
#                ).fetchall()
#            return sales
#
#def sale_exist(sale):
#    db = get_db()
#    if db.execute(f"SELECT name FROM sale WHERE name='{sale.name}'").fetchone() is not None:
#        return True
#    else:
#        return False

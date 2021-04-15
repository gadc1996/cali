from cali.lib.db import get_db

class Sale:
    """ A simple sale class """

    def __init__(self, iterable):
        self.userId = iterable['user_id']
        self.clientId = iterable['client_id']
        self.total = iterable['total']
        self.recivedCash = iterable['recivedCash']
        self.payMethodId = int(iterable['PayMethodId'])
        self.payMethod = self.get_pay_method()
        self.branchId = iterable['branch_id']

    def create_sale(self):
        return "INSERT INTO sale(user_id, client_id, total, pay_method_id) " \
        f"VALUES( {self.userId}, {self.clientId}, {self.total}, {self.payMethodId})"

    def get_change(self):
        try:
            return float(self.recivedCash) - float(self.total)
        except ValueError:
            return 0

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

#    def _is_valid(self, field, fieldName):
#        if field is None:
#            raise ValueError(f"{fieldName} Required, value: {field}")
#
#        return field
#
#    def update_sale(self, id):
#        return 'UPDATE sale '\
#            f'SET name="{self.name}", '\
#            f'contact_phone="{self.contactPhone}", '\
#            f'has_credit={self.hasCredit} '\
#            f'WHERE id={id} '
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

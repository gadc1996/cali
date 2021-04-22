from cali.lib.db import get_db
from cali.lib.article import Article
import datetime

class Credit:
    """ A simple credit class """

    def format_date(date):
        day = date[-2:]
        month = date[-5:-3]
        year = date[:4]
        date = f'{day}/{month}/{year}'
        return date

    def get_all_credits():
        db = get_db()
        credits = db.execute("""
            SELECT * FROM credit
            JOIN user on credit.user_id = user.id
            JOIN client on credit.client_id = client.id
            JOIN pay_method on credit.pay_method_id = pay_method.id
            """
        ).fetchall()
        filtered_credit = False
        return credits, filtered_credit

    def get_filtered_credits(form):
        db = get_db()
        search_date = form['date']
        search_date = Credit.format_date(search_date)

        for key, value in form.items():
            if value is '':
                continue

            if key =='id':
                credits = db.execute(f'SELECT * FROM credit WHERE {key}={value}'
                    ).fetchall()
                filtered_credit = True
                return credits, filtered_credit

            elif key =='date':
                credits = db.execute(f'SELECT * FROM credit WHERE {key}="{search_date}"'
                    ).fetchall()
                filtered_credit = True
                return credits, filtered_credit

        else:
            credits = db.execute(f'SELECT * FROM credit').fetchall()
            filtered_credit = False
            return credits, filtered_credit

    def get_remaining_time(credit):
        format = '%d/%m/%Y'
        creditDate = datetime.datetime.strptime(credit['date'], format) 
        today = datetime.datetime.now()

        creditTime = credit['credit_time']

        return creditTime - (today - creditDate).days

    def return_overdue_credit_items(remainingTime, credit):
        db = get_db()
        creditId = credit['id']
        if remainingTime <= 0:
            creditItemsSkus = Credit.get_credit_items(creditId)
            Credit.return_credit_items_to_inventory(creditItemsSkus)
            Credit.drop_credit_database(creditId)
        return


    def get_credit_items(creditId):
        db = get_db()
        creditItems = db.execute(f'SELECT * FROM credit_{creditId}_items').fetchone()
        return creditItems

    def get_id():
        db = get_db()
        credit_id = db.execute(f"SELECT id FROM credit" ).fetchall()
        if credit_id == None:
            credit_id = 1
        return len(credit_id) + 1


    def return_credit_items_to_inventory(creditItemsSkus):
        branchId = 0
        # add branch Id to credit database table
        db = get_db()
        for sku in creditItemsSkus:
            article = Article.get_article_by_sku(sku)
            stock = article[f'on_branch_{int(branchId )+ 1}']
            updateQuery = 'UPDATE article '\
                f'SET on_branch_{int(branchId) + 1}="{stock + 1}"   '\
                f'WHERE SKU={sku} '
            db.execute(updateQuery)
        db.commit()
        return

    def drop_credit_database(creditId):
        db = get_db()
        db.execute(f'DROP TABLE credit_{creditId}_items')
        db.commit()
        return

    def delete_credit(remainingTime, credit):
        if remainingTime <= 0:
            creditId = credit['id']
            db = get_db()
            db.execute(f'DELETE FROM credit WHERE id={creditId}')
            db.commit()
            return

    def save_overdue_credit_as_sale(remainingTime, credit):
        if remainingTime <= 0:
            db = get_db()
            db.execute("INSERT INTO sale(user_id, client_id, total, pay_method_id, date) " \
            f"VALUES( {credit['user_id']}, {credit['user_id']}, {credit['total']}, {credit['pay_method_id']}, '{credit['date']}')")
            db.commit()
        return


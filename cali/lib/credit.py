from flask import g, flash
from cali.lib.db import get_db
from cali.lib.article import Article
import datetime


class Credit:
    """ A simple credit class """

    def _format_date(date):
        day = date[-2:]
        month = date[-5:-3]
        year = date[:4]
        date = f'{day}/{month}/{year}'
        return date

    def _get_remaining_time_in_days(credit):
        format = '%d/%m/%Y'
        creditDate = datetime.datetime.strptime(credit['date'], format) 
        today = datetime.datetime.now()
        creditTime = credit['credit_time']
        return creditTime - (today - creditDate).days

    def _get_credit_items(creditId):
        db = get_db()
        creditItems = db.execute(f'SELECT * FROM credit_{creditId}_items').fetchone()
        return creditItems

    def _return_credit_items_to_inventory(creditItemsSkus, branchId):
        db = get_db()
        for sku in creditItemsSkus:
            article = Article.get_article_by_sku(sku)
            stock = article['stock']
            stock_on_branch = article[f'on_branch_{int(branchId )+ 1}']
            data = (stock_on_branch + 1, sku)
            query = 'UPDATE article '\
                f'SET on_branch_{int(branchId) + 1}=? '\
                f'WHERE SKU=? '
            db.execute(updateQuery)
            flash(query)
        #db.commit()
        return

    def _return_overdue_credit_items(credit):
        db = get_db()
        creditId = credit['id']
        branchId = credit['branch_id']
        creditItems = Credit._get_credit_items(creditId)
        Credit._return_credit_items_to_inventory(creditItems, branchId)
        return

    def _save_credit_as_sale(credit):
        db = get_db()
        data = (credit['user_id'], credit['branch_id'], credit['client_id'],
                credit['total'], credit['pay_method_id'], credit['date'])
        query = """
            INSERT INTO sale(user_id, branch_id, client_id,  total, pay_method_id, date)
            VALUES(?, ?, ?, ?, ?, ?)
            """
        db.execute(query, data)
        db.commit()
        return

    def _delete_credit(credit):
        creditId = credit['id']
        db = get_db()
        db.execute(f'DELETE FROM credit WHERE id={creditId}')
        db.execute(f'DROP TABLE credit_{creditId}_items')
        db.commit()
        return

    def _is_fully_payed(credit):
        total = credit['total']
        payed = credit['payed']
        return (total - payed) == 0

    def _is_pay_valid(total, payed, pay):
        return payed+pay > total or pay == 0

    def _update_payed(id, payed):
        db = get_db()
        db.execute(f'UPDATE credit SET payed={payed} WHERE id={id}')
        db.commit()
        return

    def get_all_credits():
        db = get_db()
        query = """
            SELECT * FROM credit
            JOIN user on credit.user_id = user.id
            JOIN client on credit.client_id = client.id
            JOIN pay_method on credit.pay_method_id = pay_method.id
        """
        credits = db.execute(query).fetchall()
        return credits

    def get_filtered_credits(form):
        db = get_db()
        search_date = form['date']
        if search_date:
            search_date = Credit._format_date(search_date)
            data = (search_date,)
            query = """
                    SELECT * FROM credit
                    WHERE date = ?
                """
            credits = db.execute(query, data).fetchall()
            return credits

        for key, value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM credit '\
                        f'WHERE credit.{key} = ?'
                credits = db.execute(query, data).fetchall()
                return credits

            else:
                credits = Credit.get_all_credits()
        return credits

    def update_credits_status(credits):
        for credit in credits:
            remainingTime = Credit._get_remaining_time_in_days(credit)
            if remainingTime <= 10:
                Credit._return_overdue_credit_items(credit)
                Credit._save_credit_as_sale(credit)
                Credit._delete_credit(credit)

            if Credit._is_fully_payed(credit):
                Credit._save_credit_as_sale(credit)
                Credit._delete_credit(credit)
        return

    def get_credit_by_id(id):
        db = get_db()
        credit = db.execute(f'SELECT * FROM credit WHERE id={id}').fetchone()
        return credit

    def pay_credit(credit, form):
        total = credit['total']
        payed = credit['payed']
        try:
            pay = int(form['pay'])
        except:
            pay = 0

        if Credit._is_pay_valid(total, payed, pay):
            payed += pay
            Credit._update_payed(id, payed)
        return


    def get_id():
        db = get_db()
        credit_id = db.execute(f"SELECT * FROM credit" ).fetchall()
        if credit_id == None:
            credit_id = 1
        return len(credit_id) + 1

    def drop_credit_database(creditId):
        db = get_db()
        db.commit()
        return







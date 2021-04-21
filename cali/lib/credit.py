from cali.lib.db import get_db

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

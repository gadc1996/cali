from cali.lib.db import get_db
from cali.lib.alert import Alert

class Category():
    def __init__(self, iterable):
        self.category_name = iterable['category_name']

    def _get_category_by_name(name):
        db = get_db()
        data = (name,)
        query = 'SELECT * FROM category WHERE category_name=?'
        category = db.execute(query, data).fetchone()
        return category


    def _category_exist(self):
        category = Category._get_category_by_name(self.category_name)
        return category is not None

    def is_valid(self):
        if self._category_exist():
            Alert.raise_danger_alert('Category Exist')
            return False
        else:
            return True

    def create_category(self):
        db = get_db()
        data = (self.category_name,)
        query = """
            INSERT INTO category (category_name)
            VALUES (?)
            """
        db.execute(query, data)
        db.commit()
        return

    def update_category(self, id):
        db = get_db()
        data = (self.category_name, id)
        query = """
            UPDATE category
            SET category_name=?
            WHERE id=?
            """
        db.execute(query, data)
        db.commit()
        return

    def delete_category(id):
        db = get_db()
        data = (id,)
        query = 'DELETE FROM category WHERE id=?'
        db.execute(query, data)
        db.commit()
        return

    def get_all_categories():
        db = get_db()
        query = 'SELECT * FROM category'
        categories = db.execute(query).fetchall()
        return categories

    def get_filtered_categories(form):
        db = get_db()
        for key, value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM category '\
                        f'WHERE {key}=?'
                categories = db.execute(query, data).fetchall()
                break
        else:
            categories = Category.get_all_categories()

        return categories

    def get_category_by_id(id):
        db = get_db()
        data = (id,)
        query = """
            SELECT * FROM category
            WHERE id=?
            """

        category = db.execute(query, data).fetchone()
        return category

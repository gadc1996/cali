from cali.lib.db import get_db

class Category():
    def __init__(self, iterable):
        self.category_name = iterable['name']
        self.id = self.get_category_id()

    def get_category_id(self):
        db = get_db()
        category_id = db.execute(f'SELECT id FROM category WHERE category_name="{self.category_name}"').fetchone()
        if category_id is not None:
            return category_id['id']
        else:
            category_id = db.execute(f"SELECT id FROM category").fetchall()
            return category_id[-1]['id'] + 1

    def create_category(self):
        return f"INSERT INTO category (category_name) VALUES ('{self.category_name}')"

    def delete_category(self):
        pass

    def update_category(self):
        pass

    def category_exist(self):
        db = get_db()
        if db.execute(f"SELECT * FROM category WHERE id={self.id}").fetchone() is not None:
            return True
        else:
            return False

def get_all_categories():
    db = get_db()
    categories = dict(db.execute(' SELECT * FROM category').fetchall())
    return categories

def get_single_category(id):
    db = get_db()
    category = db.execute(f'SELECT category_name FROM category WHERE id={id}').fetchone()
    return category['category_name']

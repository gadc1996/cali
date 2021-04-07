from cali.lib.db import get_db

def get_all_categories():
    db = get_db()
    categories = dict(db.execute(' SELECT * FROM category').fetchall())
    return categories

def get_single_category(id):
    db = get_db()
    category = db.execute(f'SELECT category_name FROM category WHERE id={id}').fetchone()
    return category['category_name']

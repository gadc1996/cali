from cali.lib.db import get_db
from cali.lib.category import get_all_categories, get_single_category

class Article:
    """ A simple article class """

    def __init__(self, iterable):
        self.name = self._is_valid(iterable['name'], 'name')
        self.id = self.get_article_id()
        self.description = self._is_valid(iterable['description'], 'description')
        self.price = self._is_valid(iterable['price'], 'price')
        self.sku = self._is_valid(iterable['sku'], 'sku')
        self.stock = self._is_valid(iterable['stock'], 'stock')
        self.on_branch_1 = self._is_valid(iterable['on_branch_1'], 'on_branch_1')
        self.on_branch_2 = self._is_valid(iterable['on_branch_2'], 'on_branch_2')
        self.is_regular = self._is_valid(iterable['is_regular'], 'is_regular')
        self.category_id = self._is_valid(iterable['category_id'], 'category_id')
        self.category = get_single_category(self.category_id)

    def _is_valid(self, field, fieldName):
        if field is None:
            raise ValueError(f"{fieldName} Required, value: {field}")

        return field

    def create_article(self):
        return "INSERT INTO article (name, category_id, description, price, SKU, stock, on_branch_1, on_branch_2, is_regular) " \
        f"VALUES ('{self.name}', {self.category_id}, '{self.description}', {self.price}, {self.sku}, {self.stock}, {self.on_branch_1}, {self.on_branch_2}, {self.is_regular})"

    def update_article(self):
        return 'UPDATE article '\
            f'SET name="{self.name}" ,  '\
            f'category_id=1 , '\
            f'price={self.price}, ' \
            f'SKU={self.sku} , '\
            f'on_branch_1={self.on_branch_1} , '\
            f'on_branch_2={self.on_branch_2} , '\
            f'is_regular={self.is_regular} '\
            f'WHERE id={self.id} '

    def delete_article(self):
     return f'DELETE FROM article WHERE article.id={self.id}'

    def get_article_id(self):
        db = get_db()
        article_id = db.execute(f"SELECT id FROM article WHERE name='{self.name}'").fetchone()
        if article_id is not None:
            return article_id['id']
        else:
            
            article_id = db.execute(f"SELECT id FROM article").fetchall()
            return article_id[-1]['id'] + 1

    def article_exist(self):
        db = get_db()
        if db.execute(f"SELECT name FROM article WHERE name='{self.name}'").fetchone() is not None:
            return True
        else:
            return False

def get_single_article(id):
    db = get_db()
    article = db.execute(f'SELECT * FROM article JOIN category on article.category_id = category.id WHERE article.id={id}').fetchone()
    return article

def get_all_articles():
    db = get_db()
    clients = db.execute("""
        SELECT * FROM article
        JOIN category ON article.category_id = category.id
        """
    ).fetchall()
    return clients

def get_filtered_articles(form):
    db = get_db()
    for key,value in form.items():
        if value is '':
            continue

        if key =='id':
            articles = db.execute(f'SELECT * FROM article WHERE {key}={value}'
                ).fetchall()
            return articles

        else:
            articles = db.execute(f'SELECT * FROM article WHERE {key}="{value}"'
                ).fetchall()
            return articles


from cali.lib.db import get_db

class Article:
    """ A simple article class """

    def __init__(self, iterable):
        self.name = self._is_valid(iterable['name'], 'name')
        self.category = self._is_valid(iterable['name'], 'name')
        self.description = self._is_valid(iterable['name'], 'name')
        self.price = self._is_valid(iterable['name'], 'name')
        self.sku = self._is_valid(iterable['name'], 'name')
        self.stock = self._is_valid(iterable['name'], 'name')
        self.on_branch_1 = self._is_valid(iterable['name'], 'name')
        self.on_branch_2 = self._is_valid(iterable['name'], 'name')
        self.is_regular = self._is_valid(iterable['name'], 'name')

    def _is_valid(self, field, fieldName):
        if field is None:
            raise ValueError(f"{fieldName} Required, value: {field}")

        return field

#    def create_article(self):
#        return "INSERT INTO article (name, category_id, description, price, SKU, stock, on_branch_1, on_branch_2, is_regular" \
#        f"VALUES( {self.name}, {self.category}, {self.description}, {self.price}, {self.sku}, {self.stock}, {self.on_branch_1}, {self.on_branch_2}, {self.is_regular})"
#
#    def update_client(self, id):
#        return 'UPDATE client '\
#            f'SET name="{self.name}", '\
#            f'contact_phone="{self.contactPhone}", '\
#            f'has_credit={self.hasCredit} '\
#            f'WHERE id={id} '
#
#    def delete_client(self, id):
#        return f'DELETE FROM client WHERE id={id}'
#
def get_single_article(id):
    db = get_db()
    article = db.execute(f'SELECT * FROM article WHERE id={id}').fetchone()
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

def client_exist(client):
    db = get_db()
    if db.execute(f"SELECT name FROM client WHERE name='{client.name}'").fetchone() is not None:
        return True
    else:
        return False

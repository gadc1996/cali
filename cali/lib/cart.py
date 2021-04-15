from cali.lib.db import get_db
from cali.lib.category import get_all_categories, get_single_category

class ShoppingCart:
    """ A simple shopping cart class """
    def __init__(self):
        self.price = self.get_cart_total_price()
        self.cart_items = self.get_all_cart_items()

    def get_cart_total_price(self):
        price = 0
        items = self.get_all_cart_items()
        for item in items:
            price += item['price']

        return price

    def get_cart_total_items(self):
        items = self.get_all_cart_items()
        return len(items)

    def get_all_cart_items(self):
        db = get_db()
        cart_items = db.execute("""
            SELECT * FROM cart
            """
        ).fetchall()
        return cart_items

    def clear_cart(self):
        return "DELETE FROM cart"

    def there_is_enought_stock(self, branchId):
        for cartItem in self.get_all_cart_items():
            stock = self.get_cartItem_stock(cartItem, branchId) 
            if stock == 0:
                return False

        return True

    def get_cartItem_stock(self, cartItem, branchId):
        return cartItem[f'on_branch_{int(branchId) + 1}']

class CartItem(ShoppingCart):
    """ A simple cart item class """

    def __init__(self, article):
        self.name = article['name']
        self.description = article['description']
        self.price = article['price']
        self.sku = article['sku']
        self.stock = article['stock']
        self.on_branch_1 = article['on_branch_1']
        self.on_branch_2 = article['on_branch_2']
        self.is_regular = article['is_regular']
        self.category_id = article['category_id']
        self.category = article['category_name']

#    def _is_valid(self, field, fieldName):
#        if field is None:
#            raise ValueError(f"{fieldName} Required, value: {field}")
#
#        return field
#
    def add_cart_item(self):
        return "INSERT INTO cart(name, price, SKU, stock, on_branch_1, on_branch_2, is_regular) " \
        f"VALUES ('{self.name}', {self.price}, '{self.sku}', {self.stock}, {self.on_branch_1}, {self.on_branch_2}, {self.is_regular})"


    def delete_cart_item(id):
     return f'DELETE FROM cart WHERE id={id}'
#
#
#    def update_article(self):
#        return 'UPDATE article '\
#            f'SET name="{self.name}" ,  '\
#            f'category_id=1 , '\
#            f'price={self.price}, ' \
#            f'SKU={self.sku} , '\
#            f'on_branch_1={self.on_branch_1} , '\
#            f'on_branch_2={self.on_branch_2} , '\
#            f'is_regular={self.is_regular} '\
#            f'WHERE id={self.id} '
#
#    def get_cart_item_id(self):
#        db = get_db()
#        cart_item_id = db.execute(f"SELECT id FROM cart WHERE name='{self.name}'").fetchone()
#        if article_id is not None:
#            return article_id['id']
#        else:
#            article_id = db.execute(f"SELECT id FROM article").fetchall()
#            return article_id[-1]['id'] + 1
#
#    def article_exist(self):
#        db = get_db()
#        if db.execute(f"SELECT name FROM article WHERE name='{self.name}'").fetchone() is not None:
#            return True
#        else:
#            return False
#
#def get_single_article(id):
#    db = get_db()
#    article = db.execute(f'SELECT * FROM article JOIN category on article.category_id = category.id WHERE article.id={id}').fetchone()
#    return article
#
#
#def get_filtered_articles(form):
#    db = get_db()
#    for key,value in form.items():
#        if value is '':
#            continue
#
#        if key =='id':
#            articles = db.execute(f'SELECT * FROM article WHERE {key}={value}'
#                ).fetchall()
#            return articles
#
#        else:
#            articles = db.execute(f'SELECT * FROM article WHERE {key}="{value}"'
#                ).fetchall()
#            return articles
#

from cali.lib.db import get_db
from cali.lib.category import Category
from cali.lib.article import Article
from flask import flash

class ShoppingCart:
    """ A simple shopping cart class """

    def __init__(self):
        self.price = self._get_cart_total_price()
        self.cart_items = self._get_all_cart_items()
        self.ticket = self._get_sale_ticket()

    def _get_cart_total_price(self):
        price = 0
        items = self._get_all_cart_items()
        for item in items:
            price += item['price']
        return price

    def _get_all_cart_items(self):
        db = get_db()
        query = 'SELECT * from cart'
        cart_items = db.execute(query).fetchall()
        return cart_items

    def _get_sale_ticket(self):
        ticket = {}
        cartItems = self._get_all_cart_items()
        for cartItem in cartItems:
            if cartItem['SKU'] not in ticket:
                ticket[cartItem['SKU']] = 1
            else:
                ticket[cartItem['SKU']] += 1
        return ticket

    def get_cart_total_items(self):
        items = self._get_all_cart_items()
        return len(items)

    def there_is_enought_stock(self, branchId):
        for sku, quantity in self.ticket.items():
            cartItem = Article.get_article_by_sku(sku)
            stock = self.get_cartItem_stock_on_branch(cartItem, branchId)
            if stock < quantity:
                return False

        return True

    def clear_cart(self):
        db = get_db()
        query = 'DELETE FROM cart'
        db.execute(query)
        db.commit()
        return

    def get_cartItem_stock_on_branch(self, cartItem, branchId):
        return cartItem[f'on_branch_{branchId}']

    def get_cartItem_stock(self, cartItem):
        return cartItem['stock']

    def update_cart_items_stock(self, branchId):
        db = get_db()
        ticket = self._get_sale_ticket()
        for sku, quantity in ticket.items():
            cartItem = Article.get_article_by_sku(sku)
            stock = self.get_cartItem_stock(cartItem)
            stock_on_branch = self.get_cartItem_stock_on_branch(cartItem, branchId)
            new_stock = stock - quantity
            new_stock_on_branch = stock_on_branch - quantity

            data = (new_stock_on_branch, new_stock, sku)
            query = 'UPDATE article ' \
                    f'SET on_branch_{branchId}=?, '\
                    f'stock =? '\
                    'WHERE SKU=?'

            db.execute(query, data)

        db.commit()
        return

class CartItem(ShoppingCart):
    """ A simple cart item class """

    def add_cart_item(id):
        article = Article.get_article_object_by_id(id)
        db = get_db()
        data = (article.name, article.price, article.sku,
                article.stock, article.on_branch_1, article.on_branch_2,
                article.is_regular)
        query = """
            INSERT INTO cart (name, price, SKU, stock, on_branch_1, on_branch_2, is_regular)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        db.execute(query, data)
        db.commit()
        return

    def delete_cart_item(id):
        db = get_db()
        data = (id,)
        query = """
            DELETE FROM cart WHERE id = ?
            """
        db.execute(query, data)
        db.commit()
        return

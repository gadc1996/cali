from cali.lib.db import get_db
from cali.lib.category import Category
from cali.lib.alert import Alert

class Article:
    """ A simple article class """

    def __init__(self, iterable):
        self.name = iterable['name']
        self.description = iterable['description']
        self.price = iterable['price']
        self.sku = iterable['sku']
        self.is_regular = iterable['is_regular']
        self.category_id = iterable['category_id']

        self.id = self._get_article_id()
        self.on_branch_1 = self._get_stock_on_branch(iterable, 1)
        self.on_branch_2 = self._get_stock_on_branch(iterable, 2)
        self.stock = self._get_stock()

        self.category = Category.get_category_by_id(self.category_id)

    def _get_stock(self):
        return int(self.on_branch_1) + int(self.on_branch_2)

    def _get_stock_on_branch(self, iterable, branch_id):
        stock_on_branch = iterable[f'on_branch_{branch_id}']
        try:
            return int(stock_on_branch)
        except ValueError:
            return 0

    def _get_article_id(self):
        db = get_db()
        data = (self.name,)
        query = 'SELECT id FROM article WHERE name = ?'
        article_id = db.execute(query, data).fetchone()
        if article_id is not None:
            return article_id['id']
        else:
            article_id = db.execute(f"SELECT id FROM article").fetchall()
            return article_id[-1]['id'] + 1

    def _get_article_by_name(name):
        db = get_db()
        data = (name,)
        query = 'SELECT * FROM article WHERE name=?'
        article = db.execute(query, data).fetchone()
        return article

    def _article_name_exists(self):
        article = Article._get_article_by_name(self.name)
        return article is not None

    def _is_valid(self):
        if self._article_name_exists():
            Alert.raise_danger_alert("Article Exist")
            return False
        else:
            return True

    def get_article_object_by_id(id):
        article = Article.get_article_by_id(id)
        return Article(article)

    def get_all_articles():
        db = get_db()
        query = """
            SELECT * FROM article
            JOIN category ON article.category_id = category.id
            """
        articles = db.execute(query).fetchall()
        return articles

    def get_filtered_articles(form):
        db = get_db()
        for key,value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM article '\
                        'JOIN category ON article.category_id = category.id ' \
                        f'WHERE article.{key}=?'
                articles = db.execute(query, data)
                break
        else:
            articles = Article.get_all_articles()

        return articles


    def create_article(self):
        db = get_db()
        data = (self.name, self.category_id, self.description,
                self.price, self.sku, self.stock,
                self.on_branch_1, self.on_branch_2, self.is_regular)
        query = """
            INSERT INTO article
            (name, category_id, description,
             price, SKU, stock,
             on_branch_1, on_branch_2, is_regular)
            VALUES(?,?,?,?,?,?,?,?,?)
            """
        db.execute(query, data)
        db.commit()
        return

    def get_article_by_id(id):
        db = get_db()
        data = (id,)
        query = """
            SELECT * FROM article
            JOIN category on article.category_id = category.id
            WHERE article.id = ?
        """
        article = db.execute(query, data).fetchone()
        return article

    def delete_article(id):
        db = get_db()
        data = (id,)
        query = 'DELETE FROM article WHERE id=?'
        db.execute(query, data)
        db.commit()
        return

    def update_article(self, id):
        db = get_db()
        data = (self.name, self.category_id, self.price,
                self.sku, self.stock, self.on_branch_1,
                self.on_branch_2, self.is_regular, id)
        query = """
            UPDATE article
            SET name=?,
            category_id=?,
            price=?,
            SKU=?,
            stock=?,
            on_branch_1=?,
            on_branch_2=?,
            is_regular=?
            WHERE id=?
            """

        db.execute(query, data)
        db.commit()
        return

    def get_article_by_sku(sku):
        db = get_db()
        data = (sku,)
        query = """
            SELECT * FROM article
            WHERE SKU = ?
            """
        article = db.execute(query, data).fetchone()
        return article

    def get_article_object_by_sku(sku):
        db = get_db()
        data = (sku,)
        query = """
            SELECT * FROM article
            WHERE SKU = ?
            """
        article = db.execute(query, data).fetchone()
        return Article(article)




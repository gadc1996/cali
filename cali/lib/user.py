from flask import session, redirect, url_for
from flask import flash
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.alert import Alert

class User:
    """ A simple User class """

    def __init__(self, iterable):
        self.username = iterable['username']
        self.password = generate_password_hash(iterable['password'])
        self.isSuper= iterable['is_super']
        self.canDiscount = iterable['can_discount']
        self.branchId = iterable['branch_id']

    def _user_exist(self):
        user = User._get_user_by_name(self.username)
        return user is not None

    def _get_user_by_name(name):
        db = get_db()
        data = (name,)
        query = 'SELECT * FROM user WHERE username=?'
        user = db.execute(query, data).fetchone()
        return user

    def _is_valid_login(user, password):
        if user is None:
            Alert.raise_danger_alert('Incorrect User')
            return False

        elif not check_password_hash(user['password'], password):
            Alert.raise_danger_alert('Incorrect Password')
            return False
        else:
            return True


    def is_valid(self):
        if self._user_exist():
            Alert.raise_danger_alert('User Exist')
            return False
        else:
            return True

    def create_user(self):
        db = get_db()
        data = (self.username, self.password, self.isSuper,
                      self.canDiscount, self.branchId)
        query = """
            INSERT INTO user
            (username, password, is_super, can_discount, branch_id)
            VALUES(?,?,?,?,?)
            """
        db.execute(query, data)
        db.commit()
        return

    def update_user(self, id):
        db = get_db()
        data = (self.username, self.password, self.isSuper,
                      self.canDiscount, self.branchId, id)
        query = """
            UPDATE user
            SET username=?,
            password=?,
            is_super=?,
            can_discount=?,
            branch_id=?
            WHERE id=?
            """

        db.execute(query, data)
        db.commit()
        return

    def delete_user(id):
        db = get_db()
        data = (id,)
        query = 'DELETE FROM user WHERE id=?'
        db.execute(query, data)
        db.commit()
        return

    def get_user_by_id(id):
        db = get_db()
        data = (id,)
        query = """
            SELECT * from user
            JOIN branch on user.branch_id = branch.id
            WHERE user.id=?
            """
        user = db.execute(query, data).fetchone()
        return user

    def get_all_users():
        db = get_db()
        users = db.execute("""
            SELECT * FROM user
            JOIN branch on user.branch_id = branch.id
            """).fetchall()
        return users

    def get_filtered_users(form):
        db = get_db()
        for key,value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM user '\
                        'JOIN branch on user.branch_id = branch.id '\
                        f'WHERE user.{key}=?'
                users = db.execute(query, data)
                break
        else:
            users = User.get_all_users()

        return users

    def log_in_user(form):
        db = get_db()
        username = form['username']
        password = form['password']
        user = User._get_user_by_name(username)
        if User._is_valid_login(user, password):
            flash("inside login")
            session.clear()
            session['user_id'] = user['id']
        return

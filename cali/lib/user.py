from cali.lib.db import get_db

class User:
    """ A simple User class """

    def __init__(self, iterable):
        self.username = self._is_valid(iterable['username'], 'Username')
        self.password = self._is_valid(iterable['password'], 'Password')
        self.isSuper= self._is_valid(iterable['is_super'], 'is_super')
        self.canDiscount = self._is_valid(iterable['can_discount'], 'can_discount')
        self.branchId = self._is_valid(iterable['branch_id'], 'branch_id')

    def _is_valid(self, field, fieldName):
        if field is None:
            raise ValueError(f"{fieldName} Required, value: {field}")

        return field

    def create_user(self):
        return "INSERT INTO user (username, password, is_super, can_discount, branch_id) " \
        f"VALUES('{self.username}', '{self.password}', {self.isSuper}, {self.canDiscount}, {self.branchId})"

    def update_user(self, id):
        return 'UPDATE user '\
            f'SET username="{self.username}", '\
            f'password="{self.password}", '\
            f'is_super={self.isSuper}, '\
            f'can_discount={self.canDiscount}, '\
            f'branch_id={self.branchId} '\
            f'WHERE id={id} '

    def delete_user(self, id):
        return f'DELETE FROM user WHERE id={id}'

def get_single_user(id):
    db = get_db()
    user = db.execute(f'SELECT username, password, is_super, can_discount, branch_id FROM user JOIN branch on user.branch_id = branch.id WHERE user.id={id}').fetchone()
    return user

def get_all_users():
    db = get_db()
    users = db.execute("""
        SELECT * FROM user
        JOIN branch on user.branch_id = branch.id
        """
    ).fetchall()
    return users

def get_filtered_users(form):
    db = get_db()
    for key,value in form.items():
        if value is '':
            continue

        if key =='id':
            users = db.execute('SELECT * FROM user '\
                'JOIN branch on user.branch_id = branch.id '\
                f'WHERE user.{key}={value}'
                ).fetchall()
            return users

        else:
            users = db.execute(f'SELECT * FROM user JOIN branch on user.branch_id = branch.id WHERE user.{key}="{value}" '
                ).fetchall()
            return users


def user_exist(user):
    db = get_db()
    if db.execute(f"SELECT username FROM user WHERE username='{user.username}'").fetchone() is not None:
        return True
    else:
        return False

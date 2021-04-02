class User:
    """ A simple example class """

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

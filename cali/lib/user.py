class User:
    """ A simple example class """

    def __init__(self, iterable):
        self.username = self._is_valid(iterable['username'], 'Username')
        self.password = self._is_valid(iterable['password'], 'Password')
        self.isSuper= self._is_valid(iterable['is_super'], 'is_super')
        self.canDiscount = self._is_valid(iterable['can_discount'], 'can_discount')
        self.branchId = self._is_valid(iterable['branch_id'], 'branch_id')

    def _is_valid(self, field, fieldName):
        if not field:
            raise ValueError(f"{fieldName} Required")

        return field

    def create_user(self):
        return "INSERT INTO user (username, password, is_super, can_discount, branch_id) " \
        f"VALUES('{self.username}', '{self.password}', {self.isSuper}, {self.canDiscount}, {self.branchId})"


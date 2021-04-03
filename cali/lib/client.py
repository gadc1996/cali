class Client:
    """ A simple client class """

    def __init__(self, iterable):
        self.name = self._is_valid(iterable['name'], 'name')
        self.contactPhone = self._is_valid(iterable['contact_phone'], 'Contact Phone')
        self.hasCredit = self._is_valid(iterable['has_credit'], 'Has Credit')

    def _is_valid(self, field, fieldName):
        if field is None:
            raise ValueError(f"{fieldName} Required, value: {field}")

        return field

    def create_client(self):
        return "INSERT INTO client (name, contact_phone, has_credit) " \
        f"VALUES( {self.name}, {self.contactPhone}, {self.hasCredit})"

    def update_client(self, id):
        return 'UPDATE client '\
            f'SET name="{self.name}", '\
            f'contact_phone="{self.contactPhone}", '\
            f'has_credit={self.hasCredit} '\
            f'WHERE id={id} '

    def delete_client(self, id):
        return f'DELETE FROM client WHERE id={id}'

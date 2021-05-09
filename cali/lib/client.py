from cali.lib.db import get_db
from cali.lib.alert import Alert

class Client:
    """ A simple client class """

    def __init__(self, iterable):
        self.name = iterable['name']
        self.contact_phone = iterable['contact_phone']
        self.has_credit = iterable['has_credit']

    def _client_exist(self):
        client = Client._get_client_by_name(self.name)
        return client is not None

    def _get_client_by_name(name):
        db = get_db()
        data = (name,)
        query = 'SELECT * FROM client WHERE name=?'
        client = db.execute(query, data).fetchone()
        return client

    def _contact_phone_is_valid(self):
        return self.contact_phone.isnumeric()

    def _name_is_valid(self):
        return self.name.isalpha()

    def _is_valid(self):
        if not self._name_is_valid():
            Alert.raise_danger_alert('Invalid Name, Please use only letters')
        elif not self._contact_phone_is_valid():
            Alert.raise_danger_alert('Invalid Phone Number, Please use only numbers')
        else:
            return True
        return False

    def is_valid_update(self):
        return self._is_valid()

    def is_valid_create(self):
        if self._client_exist():
            Alert.raise_danger_alert('Client Exist')
        elif not self._is_valid():
            pass
        else:
            return True

        return False


    def create_client(self):
        db = get_db()
        data = (self.name, self.contact_phone, self.has_credit)
        query = """
            INSERT INTO client (name, contact_phone, has_credit)
            VALUES (?, ?, ?)
            """
        db.execute(query, data)
        db.commit()
        return

    def update_client(self, id):
        db = get_db()
        data = (self.name, self.contact_phone,
                      self.has_credit, id)
        query = """
            UPDATE client
            SET name=?,
            contact_phone=?,
            has_credit=?
            WHERE id=?
            """

        db.execute(query, data)
        db.commit()
        return

    def delete_client(id):
        db = get_db()
        data = (id,)
        query =  'DELETE FROM client WHERE id=?'
        db.execute(query, data)
        db.commit()
        return

    def get_all_clients():
        db = get_db()
        query = 'SELECT * FROM client'
        clients = db.execute(query).fetchall()
        return clients

    def get_filtered_clients(form):
        db = get_db()
        for key,value in form.items():
            if value:
                data = (value,)
                query = 'SELECT * FROM client '\
                        f'WHERE {key}=?'
                clients = db.execute(query, data).fetchall()
                break
        else:
            clients = Client.get_all_clients()

        return clients

    def get_client_by_id(id):
        db = get_db()
        data = (id,)
        query = 'SELECT * FROM client WHERE id=?'
        client = db.execute(query, data).fetchone()
        return client

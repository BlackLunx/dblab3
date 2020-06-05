import psycopg2
from sqlfunctions import functions, creating
def get_connection(dbname, user, password):
    connection = psycopg2.connect(
        database=dbname,
        user=user,
        password=password,
        host="127.0.0.1",
        port="5432"
    )
    connection.autocommit = True
    return connection


class Database:
    def __init__(self, user='postgres', password='postgres'):
        self.connection = get_connection('postgres', user, password)
        self.c = self.connection.cursor()
        self.c.execute(creating)
        self.c.execute(f'''SELECT create_database()''')
        self.c.close()
        self.connection.close()
        self.connection = get_connection('lab', 'lab_user', 'lab_user')
        self.c = self.connection.cursor()
        self.c.execute(functions)

    def __del__(self):
        self.c.close()
        self.connection.close()

    def show_clothes(self, _id=-1, brand = '', size = '', cost=-1):
        self.c.execute(f"""SELECT * FROM show_clothes({_id}, '{brand}', '{size}', money({cost}))""")

    def insert_clothes(self, brand, size, cost):
        self.c.execute(f"""SELECT insert_clothes('{brand}', '{size}', money({cost}))""")

    def get_count_clothes(self, _id=-1, brand='', size='', cost=-1):
        self.c.execute(f"""SELECT count_clothes({_id}, '{brand}', '{size}', money({cost}))""")

    def delete_clothes(self, _id=-1, brand='', size='', cost=-1):
        self.c.execute(f"""SELECT delete_clothes({_id}, '{brand}', '{size}', money({cost}))""")

    def show_location(self, brand='', place=''):
        self.c.execute(f"""SELECT * FROM show_location('{brand}', '{place}')""")
        
    def insert_location(self, brand='', place=''):
        self.c.execute(f"""SELECT insert_location('{brand}', '{place}')""")

    def get_count_location(self, brand='', place=''):
        self.c.execute(f"""SELECT count_location('{brand}', '{place}')""")

    def delete_location(self, brand='', place=''):
        self.c.execute(f"""SELECT delete_location('{brand}', '{place}')""")

    def erase_clothes(self):
        self.c.execute(f'''SELECT truncate_clothes()''')

    def erase_location(self):
        self.c.execute(f'''SELECT truncate_location()''')

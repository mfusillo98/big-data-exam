import mysql.connector
class QueryBuilder:
    def __init__(self, host, user, password, database, port=3306):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.query = None
        self.params = None

    def select(self, table, columns='*'):
        self.query = f"SELECT {columns} FROM {table}"
        self.params = []
        return self

    def join(self, table, on_condition):
        self.query += f" JOIN {table} ON {on_condition}"
        return self

    def where(self, conditions, *args):
        self.query += f" WHERE {conditions}"
        self.params.extend(args)
        return self

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join('%s' for _ in data.values())
        self.query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.params = list(data.values())
        return self

    def update(self, table, data):
        updates = ', '.join(f"{key} = %s" for key in data.keys())
        self.query = f"UPDATE {table} SET {updates}"
        self.params = list(data.values())
        return self

    def delete(self, table):
        self.query = f"DELETE FROM {table}"
        self.params = []
        return self

    def execute(self, return_lastrowid=False):
        self.cursor.execute(self.query, self.params)
        self.connection.commit()

        if return_lastrowid:
            return self.cursor.lastrowid

    def fetch_all(self):
        self.cursor.execute(self.query)
        for row in self.cursor.fetchall():
            yield row

    def fetch_one(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()
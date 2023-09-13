import sqlite3


class Queries:

    def __init__(self):
        self.connection = sqlite3.connect('my_database_client.db')
        self._check_or_create_map()

    def _check_or_create_map(self):
        cursor = self._get_cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Map (
                id INTEGER PRIMARY KEY,
                map_name TEXT NOT NULL,
                cost INTEGER NOT NULL,
                count INTEGER NOT NULL
            );"""
        )
        self._save()

    def sql_select(self, query: str):
        try:
            cursor = self._get_cursor()
            return cursor.execute(query).fetchall()
        except sqlite3.OperationalError as ex:
            print(ex)
            return []

    def sql_insert(self, query: str, *args):
        cursor = self._get_cursor()
        cursor.execute(query, *args)
        self._save()

    def _get_cursor(self):
        return self.connection.cursor()

    def _save(self):
        self.connection.commit()

    def __del__(self):
        try:
            self.connection.close()
        except Exception:
            pass

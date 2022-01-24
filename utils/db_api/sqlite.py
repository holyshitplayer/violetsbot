import sqlite3
from typing import List


def sqlite_lower(value_):
    return value_.lower()


def sqlite_upper(value_):
    return value_.upper()


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.create_function("LOWER", 1, sqlite_lower)
        connection.create_function("UPPER", 1, sqlite_upper)
        cursor = connection.cursor()

        data = None
        cursor.execute(sql, parameters)
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        if commit:
            connection.commit()

        connection.close()
        return data

    def execute_many(self, sql: str, values_list: List[tuple]):
        connection = self.connection
        cursor = connection.cursor()
        cursor.executemany(sql, values_list)
        connection.commit()
        connection.close()

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        sql += ";"
        return sql, tuple(parameters.values())

    @staticmethod
    def filter_sorts(sql):
        filters = ["??", "харьков", " или ", "/", "безымяшка", "none", " и ", "рынок", "валя", "наташа", "малиново",
                   "краем", "каймой"]
        sql += " AND `name` NOT LIKE ".join([
            f"'%{item}%'" for item in filters
        ])
        sql += ";"
        return sql

    def create_table_sorts(self):
        sql = "CREATE TABLE IF NOT EXISTS sorts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `name` VARCHAR(255) NOT NULL UNIQUE COLLATE NOCASE);"
        self.execute(sql, commit=True)

    def create_table_kids(self):
        sql = "CREATE TABLE IF NOT EXISTS kids (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sort_id INT NOT NULL, list VARCHAR(255) NOT NULL, quantity INT NOT NULL, FOREIGN KEY (sort_id) REFERENCES sorts ON DELETE CASCADE);"
        self.execute(sql, commit=True)

    def create_table_starters(self):
        sql = "CREATE TABLE IF NOT EXISTS starters (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sort_id INT NOT NULL, list VARCHAR(255) NOT NULL, quantity INT NOT NULL, FOREIGN KEY (sort_id) REFERENCES sorts ON DELETE CASCADE);"
        self.execute(sql, commit=True)

    def create_table_orders(self):
        sql = "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sort_id INT NOT NULL, list VARCHAR(255) NOT NULL, quantity INT NOT NULL, FOREIGN KEY (sort_id) REFERENCES sorts ON DELETE CASCADE);"
        self.execute(sql, commit=True)

    def drop_table_sorts(self):
        sql = "DROP TABLE IF EXISTS sorts;"
        self.execute(sql, commit=True)

    def drop_table_kids(self):
        sql = "DROP TABLE IF EXISTS kids;"
        self.execute(sql, commit=True)

    def drop_table_starters(self):
        sql = "DROP TABLE IF EXISTS starters;"
        self.execute(sql, commit=True)

    def drop_table_orders(self):
        sql = "DROP TABLE IF EXISTS orders;"
        self.execute(sql, commit=True)

    def fill_table_sorts(self, values: List[tuple]):
        sql = "INSERT INTO sorts (name) VALUES (?);"
        self.execute_many(sql, values)

    def fill_table_kids(self, values: List[tuple]):
        sql = "INSERT INTO kids (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def fill_table_starters(self, values: List[tuple]):
        sql = "INSERT INTO starters (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def fill_table_orders(self, values: List[tuple]):
        sql = "INSERT INTO orders (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def refill_table_sorts(self, values: List[tuple]):
        self.execute("DELETE FROM sorts;", commit=True)
        sql = "INSERT INTO sorts (name) VALUES (?);"
        self.execute_many(sql, values)

    def refill_table_kids(self, values: List[tuple]):
        self.execute("DELETE FROM kids;", commit=True)
        sql = "INSERT INTO kids (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def refill_table_starters(self, values: List[tuple]):
        self.execute("DELETE FROM starters;", commit=True)
        sql = "INSERT INTO starters (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def refill_table_orders(self, values: List[tuple]):
        self.execute("DELETE FROM orders;", commit=True)
        sql = "INSERT INTO orders (sort_id, list, quantity) VALUES (?, ?, ?);"
        self.execute_many(sql, values)

    def select_sort(self, **kwargs):
        sql = "SELECT * FROM sorts WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_filtered_sorts(self):
        sql = "SELECT * FROM sorts WHERE `name` NOT LIKE "
        sql = self.filter_sorts(sql)
        return self.execute(sql, fetchall=True)

    def select_sort_in_kids(self, sort_id: int):
        sql = "SELECT list, quantity FROM kids WHERE sort_id = ?;"
        return self.execute(sql, parameters=(sort_id,), fetchall=True)

    def select_sort_in_starters(self, sort_id: int):
        sql = "SELECT list, quantity FROM starters WHERE sort_id = ?;"
        return self.execute(sql, parameters=(sort_id,), fetchall=True)

    def select_sort_in_orders(self, sort_id: int):
        sql = "SELECT list, quantity FROM orders WHERE sort_id = ?;"
        return self.execute(sql, parameters=(sort_id,), fetchall=True)

    def sort_find(self, query: str):
        sql = f"SELECT * FROM sorts WHERE LOWER(`name`) LIKE LOWER('%{query}%');"
        return self.execute(sql, fetchall=True)

    def sort_count_kids(self, sort_id):
        sql = "SELECT SUM(sort.quantity) FROM (SELECT * FROM kids WHERE sort_id = ?) AS sort;"
        result = self.execute(sql, parameters=(sort_id,), fetchone=True)[0]
        count = result if result else 0
        return count

    def sort_count_starters(self, sort_id: int):
        sql = "SELECT SUM(sort.quantity) FROM (SELECT * FROM starters WHERE sort_id = ?) AS sort;"
        result = self.execute(sql, parameters=(sort_id,), fetchone=True)[0]
        count = result if result else 0
        return count

    def sort_count_orders(self, sort_id: int):
        sql = "SELECT SUM(sort.quantity) FROM (SELECT * FROM orders WHERE sort_id = ?) AS sort;"
        result = self.execute(sql, parameters=(sort_id,), fetchone=True)[0]
        count = result if result else 0
        return count

    def count_sorts(self):
        sql = "SELECT COUNT(*) FROM sorts WHERE `name` NOT LIKE "
        sql = self.filter_sorts(sql)
        result = self.execute(sql, fetchone=True)[0]
        count = result if result else 0
        return count

    def count_kids(self):
        sql = "SELECT SUM(quantity) FROM kids;"
        result = self.execute(sql, fetchone=True)[0]
        count = result if result else 0
        return count

    def count_starters(self):
        sql = "SELECT SUM(quantity) FROM starters;"
        result = self.execute(sql, fetchone=True)[0]
        count = result if result else 0
        return count

    def count_orders(self):
        sql = "SELECT SUM(quantity) FROM orders;"
        result = self.execute(sql, fetchone=True)[0]
        count = result if result else 0
        return count

    def list_titles_kids(self):
        sql = "SELECT DISTINCT list FROM kids;"
        return self.execute(sql, fetchall=True)

    def list_titles_starters(self):
        sql = "SELECT DISTINCT list FROM starters;"
        return self.execute(sql, fetchall=True)

    def list_titles_orders(self):
        sql = "SELECT DISTINCT list FROM orders;"
        return self.execute(sql, fetchall=True)

    def list_content_kids(self, list_title: str):
        sql = "SELECT sort_id, quantity FROM kids WHERE list = ?;"
        return self.execute(sql, parameters=(list_title,), fetchall=True)

    def list_content_starters(self, list_title: str):
        sql = "SELECT sort_id, quantity FROM starters WHERE list = ?;"
        return self.execute(sql, parameters=(list_title,), fetchall=True)

    def list_content_orders(self, list_title: str):
        sql = "SELECT sort_id, quantity FROM orders WHERE list = ?;"
        return self.execute(sql, parameters=(list_title,), fetchall=True)

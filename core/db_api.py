import os
import sqlite3

db = os.getenv('SQLITE3_FILE')


def create_tables():
    with sqlite3.connect(db) as session:
        cursor = session.cursor()
        cursor.execute("drop table if exists users")
        cursor.execute("""create table if not exists users (
            id integer primary key,
            username text,
            balance integer
        )""")


def add_default_data():
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        values = [('Bob', 5000), ('Ivan', 6334), ('Petr', 11992), ('Yaroslav', 9285), ('Dmitry', 15000)]
        for val in values:
            cursor.execute("insert into users (username, balance) values (?,?)", val)


def insert(**kwargs):
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        values = (kwargs['username'], kwargs['balance'])
        cursor.execute("insert into users (username, balance) values (?, ?)", values)


def drop(user_id: int):
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        cursor.execute("delete from users where id=?", (user_id,))


def update_username(**kwargs):
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        values = (kwargs['username'], kwargs['id'])
        cursor.execute("update users set username=? where id=?", values)


def update_balance(**kwargs):
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        values = (kwargs['balance'], kwargs['id'])
        cursor.execute("update users set balance=? where id=?", values)


def select_by_username(username: str) -> tuple:
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        result = cursor.execute("select * from users where username=?", (username,))
        return result.fetchone()


def select_by_id(user_id: int) -> tuple:
    with sqlite3.connect(db) as session:
        cursor = session.cursor()

        result = cursor.execute("select * from users where id=?", (user_id,))
        return result.fetchone()


# def select_all():
#     with sqlite3.connect(db) as session:
#         cursor = session.cursor()
#
#         result = cursor.execute("select * from users")
#         return result.fetchall()


def db_init():
    create_tables()
    add_default_data()


if __name__ == '__main__':
    db_init()

import sqlite3
from sqlite3 import Cursor


def connect_gracefully(func: callable) -> callable:
    """Декоратор для безопасного подключения к бд."""

    def inner(**kwargs):
        with sqlite3.connect("sqlite_python.db") as connection:
            cursor = connection.cursor()
            kwargs["cursor"] = cursor
            return func(**kwargs)

    return inner


@connect_gracefully
def execute_functions(cursor: Cursor) -> callable:
    """
    Функция запускающая функционал модуля.

    :param cursor: курсор подключения к базе данных
    """
    users_list = [
        ("Иван",),
        ("Константин",),
        ("Дмитрий",),
        ("Александр",),
    ]

    products_list = [
        ("Мяч", 299.99),
        ("Ручка", 18),
        ("Кружка", 159.87),
        ("Монитор", 18000),
        ("Телефон", 9999.9),
        ("Кофе", 159),
    ]

    orders_client_list = [2, 2, 2, 1, 1, 1, 1, 4, 3, 3, 1]
    orders_product_list = [2, 5, 1, 1, 3, 6, 2, 5, 6, 3, 5]
    orders_name_list = [f"Закупка {i}" for i in range(1, 12)]
    orders_list = list(zip(orders_client_list, orders_product_list, orders_name_list))

    fill_db(users=users_list, products=products_list, orders=orders_list, cursor=cursor)
    print(return_clients_with_purchases_sum(cursor))
    print(return_clients_who_bought_phone(cursor))
    print(return_customs_count_by_name(cursor))


def fill_db(users: list[tuple], products: list[tuple], orders: list[tuple], cursor: Cursor) -> None:
    """
    Функция заполняющая базу данных.

    :param users: объекты на заполнения таблицы clients
    :param products: объекты на заполнения таблицы products
    :param orders: объекты на заполнения таблицы orders
    :param cursor: курсор подключения к базе данных
    """
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS clients
        (client_id INTEGER PRIMARY KEY AUTOINCREMENT, client_name CHAR);"""
    )

    cursor.executemany(
        """INSERT INTO clients(client_name) VALUES (?);""",
        users,
    )

    cursor.connection.commit()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS products
        (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name CHAR, price REAL);"""
    )

    cursor.executemany(
        """INSERT INTO products(product_name, price) VALUES (?, ?);""",
        products,
    )

    cursor.connection.commit()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS orders
        (order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INT, product_id INT, order_name CHAR,
        CONSTRAINT fk_client FOREIGN KEY (client_id)
        REFERENCES clients (client_id)
        ON DELETE CASCADE,
        CONSTRAINT fk_product FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE);"""
    )

    cursor.executemany(
        """INSERT INTO orders(client_id, product_id, order_name) VALUES (?, ?, ?);""",
        orders,
    )
    cursor.connection.commit()


def return_clients_with_purchases_sum(cursor: Cursor) -> list[tuple]:
    """
    Возвращает список клиентов с общей суммой их покупки.

    :param cursor: курсор подключения к базе данных
    :returns: список клиентов с общей суммой их покупки
    """
    cursor.execute(
        """SELECT client_name, SUM(price)
        FROM (SELECT client_id, price
        FROM orders LEFT JOIN products
        ON orders.product_id = products.product_id) AS gr
        LEFT JOIN clients
        ON clients.client_id = gr.client_id
        GROUP BY client_name;"""
    )
    return cursor.fetchall()


def return_clients_who_bought_phone(cursor: Cursor) -> list[tuple]:
    """
    Возвращает список клиентов, которые купили телефон.

    :param cursor: курсор подключения к базе данных
    :returns: список клиентов, которые купили телефон
    """
    cursor.execute(
        """SELECT client_name
        FROM (SELECT client_id, product_name
        FROM orders LEFT JOIN products
        ON orders.product_id = products.product_id) AS gr
        LEFT JOIN clients
        ON clients.client_id = gr.client_id
        WHERE product_name='Телефон';"""
    )
    return cursor.fetchall()


def return_customs_count_by_name(cursor: Cursor) -> list[tuple]:
    """
    Возвращает список товаров с количеством их заказа.

    :param cursor: курсор подключения к базе данных
    :returns: список товаров с количеством их заказа
    """
    cursor.execute(
        """SELECT product_name, COUNT(product_name)
        FROM orders LEFT JOIN products
        ON orders.product_id = products.product_id
        GROUP BY product_name;
        """
    )
    return cursor.fetchall()


if __name__ == "__main__":
    execute_functions()

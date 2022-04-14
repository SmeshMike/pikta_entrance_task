import sqlite3
from sqlite3 import Cursor


def connect_graceful(func: callable) -> callable:
    """Decorator for graceful connection to database."""

    def inner():
        with sqlite3.connect("sqlite_python.db") as connection:
            cursor = connection.cursor()
            return func(cursor)

    return inner


@connect_graceful
def fill_db(cursor: Cursor) -> None:
    """
    Fulfilling database function.

    :param cursor: database connection cursor
    """
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS clients
        (client_id INTEGER PRIMARY KEY AUTOINCREMENT, client_name CHAR);"""
    )

    cursor.execute(
        """INSERT INTO clients (client_name)
        VALUES ('Иван'), ('Константин'), ('Дмитрий'), ('Александр');
        """
    )

    cursor.connection.commit()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS products
        (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name CHAR, price REAL);"""
    )

    products_list = [
        ("Мяч", 299.99),
        ("Ручка", 18),
        ("Кружка", 159.87),
        ("Монитор", 18000),
        ("Телефон", 9999.9),
        ("Кофе", 159),
    ]
    cursor.executemany(
        """INSERT INTO products(product_name, price) VALUES (?, ?);
        """,
        products_list,
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
        ON DELETE CASCADE
        );"""
    )

    orders_client_list = [2, 2, 2, 1, 1, 1, 1, 4, 3, 3, 1]
    orders_product_list = [2, 5, 1, 1, 3, 6, 2, 5, 6, 3, 5]
    orders_name_list = [f"Закупка {i}" for i in range(1, 12)]
    orders_list = list(zip(orders_client_list, orders_product_list, orders_name_list))
    cursor.executemany(
        """INSERT INTO orders(client_id, product_id, order_name) VALUES (?, ?, ?);
        """,
        orders_list,
    )
    cursor.connection.commit()


@connect_graceful
def show_clients_with_purchases_sum(cursor: Cursor) -> list[tuple]:
    """
    Shows clients with a sum of their purchases.

    :param cursor: database connection cursor
    :returns: list of clients
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


@connect_graceful
def show_clients_who_bought_phone(cursor: Cursor) -> list[tuple]:
    """
    Shows clients who bought phone.

    :param cursor: database connection cursor
    :returns: list of clients
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


@connect_graceful
def show_customs_count_by_name(cursor: Cursor) -> list[tuple]:
    """
    Shows count of bought purchases by purchase name.

    :param cursor: database connection cursor
    :returns: list of purchases with count
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
    fill_db()
    print(show_clients_with_purchases_sum())
    print(show_clients_who_bought_phone())
    print(show_customs_count_by_name())

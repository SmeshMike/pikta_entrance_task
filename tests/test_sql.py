import os
import sqlite3
import sys

import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, ".."))

import sql_task as st


@pytest.mark.parametrize(
    "users_input,products_input,orders_input",
    [
        ([("Иван",)], [("Мяч", 299.99)], [(1, 1, "Закупка 1")]),
        (
            [("Иван",), ("Константин",)],
            [("Мяч", 299.99), ("Ручка", 18)],
            [(1, 1, "Закупка 1"), (2, 2, "Закупка 2")],
        ),
    ],
)
def test_fill_db(users_input, products_input, orders_input):
    with sqlite3.connect(":memory:") as connection:
        cursor = connection.cursor()
        st.fill_db(users_input, products_input, orders_input, cursor)
        cursor.execute("""SELECT COUNT(client_name) FROM clients;""")
        clients_count = int(*cursor.fetchone())
        assert clients_count == len(users_input)
        cursor.execute("""SELECT COUNT(product_name) FROM products;""")
        products_count = int(*cursor.fetchone())
        assert products_count == len(products_input)
        cursor.execute("""SELECT COUNT(order_name) FROM orders;""")
        orders_count = int(*cursor.fetchone())
        assert orders_count == len(orders_input)


@pytest.mark.parametrize(
    "users_input,products_input,orders_input",
    [
        ([("Иван",)], [("Мяч", 299.99)], [(1, 1, "Закупка 1")]),
        (
            [("Иван",), ("Константин",)],
            [("Мяч", 299.99), ("Ручка", 18)],
            [(1, 1, "Закупка 1"), (2, 2, "Закупка 2")],
        ),
    ],
)
def test_return_clients_with_purchases_sum(users_input, products_input, orders_input):
    with sqlite3.connect(":memory:") as connection:
        cursor = connection.cursor()
        st.fill_db(users_input, products_input, orders_input, cursor)
        clients = st.return_clients_with_purchases_sum(cursor)
        for i, v in enumerate(clients):
            assert v[0] == users_input[i][0]
            assert v[1] == products_input[i][1]


@pytest.mark.parametrize(
    "users_input,products_input,orders_input",
    [
        ([("Иван",)], [("Телефон", 9999.9)], [(1, 1, "Закупка 1")]),
        (
            [("Иван",), ("Константин",)],
            [("Телефон", 9999.9), ("Ручка", 18)],
            [(1, 1, "Закупка 1"), (2, 2, "Закупка 2")],
        ),
    ],
)
def test_return_clients_who_bought_phone(users_input, products_input, orders_input):
    with sqlite3.connect(":memory:") as connection:
        cursor = connection.cursor()
        st.fill_db(users_input, products_input, orders_input, cursor)
        clients = st.return_clients_who_bought_phone(cursor)
        assert clients[0][0] == "Иван"


@pytest.mark.parametrize(
    "users_input,products_input,orders_input",
    [
        ([("Иван",)], [("Телефон", 9999.9)], [(1, 1, "Закупка 1")]),
        (
            [("Иван",), ("Константин",)],
            [("Телефон", 9999.9), ("Ручка", 18)],
            [(1, 1, "Закупка 1"), (2, 2, "Закупка 2")],
        ),
    ],
)
def test_return_customs_count_by_name(users_input, products_input, orders_input):
    with sqlite3.connect(":memory:") as connection:
        cursor = connection.cursor()
        st.fill_db(users_input, products_input, orders_input, cursor)
        customs = st.return_customs_count_by_name(cursor)
        assert len(customs) == len(products_input)
        for v in customs:
            assert int(v[1]) == 1

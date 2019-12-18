"""
CRUD properties implementation
"""
import errors.errors as errors
from base64 import b64encode
import requests


def add(conn, product_name: str, price: int, img: str, category_id: int) -> None:
    """
    Add new product to db.
    :param conn: str
    :param product_name: str
    :param price: int
    :param img: str-> URL to image
    :param category_id: int
    :return: None
    """

    # download having img as URL to binary variable
    # save content of such variable into bytea field
    response = requests.get(img)

    with conn.cursor() as cursor:
        cursor.execute("""insert into products(name, price, image, category_id)
                            values ('{0}', '{1}', '{2}','{3}')""".format(product_name, price, response.content, category_id))
    conn.commit()


def get_product(conn, product_id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param product_id: int
    :return: str
    """
    with conn.cursor() as cursor:
        cursor.execute("""select name from products
                                where id = {0}""".format(product_id))
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise errors.StoreError


def get_product_price(con, product_id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param product_id: int
    :return: str
    """
    with con.cursor() as cursor:
        cursor.execute("""select price from products
                            where id = {0}""".format(product_id))
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise errors.StoreError

def get_product_image(con, product_id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param product_id: int
    :return: str
    """
    with con.cursor() as cursor:
        cursor.execute("""select Image from products
                            where id = {0}""".format(product_id))
        try:
            return b64encode(cursor.fetchone()[0]).decode("utf-8")
        except TypeError:
            raise errors.StoreError


def edit_product(conn, product_id: int, new_price: int) -> None:
    """
    Update task in db.
    :param conn: str
    :param new_price: int
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute("""update products
                        set price = '{0}'
                        where id = '{1}'""".format(new_price, product_id))
        if cursor.rowcount:
            conn.commit()
        else:
            raise errors.StoreError


def delete_product(conn, product_id: int) -> None:
    """
    Delete task in db.
    :param conn: str
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute("""delete from products 
                        where id = {0}""".format(product_id))
        if cursor.fetchone():
            conn.commit()
        else:
            raise errors.StoreError

import mariadb


def db_connection():
    connection = mariadb.connect(
        user="root",
        password="Bu@1234#Li",
        host="localhost",
        port=3306,
        database="zombiator",
        autocommit=True
    )

    cursor = connection.cursor()
    return cursor


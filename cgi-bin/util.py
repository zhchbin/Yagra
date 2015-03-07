from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from MySQLdb import connect


def connect_db():
    return connect('localhost', MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

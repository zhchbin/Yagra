from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from MySQLdb import connect

import json
import sys


def connect_db():
    return connect('localhost', MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


def dump_response_and_exit(success, message):
    response = {}
    response['success'] = success
    response['message'] = message
    print json.dumps(response)
    sys.exit(0)

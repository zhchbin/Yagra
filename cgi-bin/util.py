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


def print_html_and_exit(message):
    print """\
Content-Type: text/html\n
<html>
<body>
    <p>%s</p>
</body>
</html>
    """ % (message,)
    sys.exit(0)


def forbidden():
    print 'Status: 403 Forbidden'
    print "Content-Type: text/html"
    print
    print "403 Forbidden"
    sys.exit(0)

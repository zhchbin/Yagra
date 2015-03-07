#!/usr/bin/python

from MySQLdb import Error
from util import connect_db, dump_response_and_exit

import cgi
import hashlib
import json
import re
import sys


print "Content-type:applicaion/json\r\n\r\n"
form = cgi.FieldStorage()
username = form.getvalue('username')
password = form.getvalue('password')
if username is None or password is None:
    dump_response_and_exit(False, 'Missing field: username or password.')

if re.match(r"^[a-zA-Z0-9_.-]+$", username) is None:
    dump_response_and_exit(False, 'Invalid username.')

if re.match(r'[A-Za-z0-9@#$%^&+=_.-]{6,}', password) is None:
    dump_response_and_exit(False, 'Invalid password.')

try:
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO User values (%s, %s)",
                    (username, hashlib.sha1(password).digest()))
        con.commit()
        dump_response_and_exit(True, 'Done.')
except Error, e:
    if con:
        con.rollback()
    dump_response_and_exit(False, e[1])
finally:
    con.close()

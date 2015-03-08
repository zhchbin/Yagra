#!/usr/bin/python

from util import connect_db, dump_response_and_exit, forbidden
from MySQLdb import Error

import Cookie
import os

if 'HTTP_COOKIE' not in os.environ:
    forbidden()

cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SmartCookie()
cookie.load(cookie_string)
if '_yagra_session' not in cookie:
    forbidden()


session_id = cookie['_yagra_session'].value
con = connect_db()
try:
    cur = con.cursor()
    cur.execute("SELECT username FROM Session WHERE id=%s", (session_id,))
    data = cur.fetchall()
    if len(data) == 0:
        forbidden()
    username = data[0][0]
    print "Content-type:applicaion/json"
    print
    dump_response_and_exit(True, username)
except Error, e:
    dump_response_and_exit(False, e[1])

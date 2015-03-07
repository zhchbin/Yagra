#!/usr/bin/python

from util import connect_db, dump_response_and_exit
from MySQLdb import Error

import Cookie
import cgi
import os

if 'HTTP_COOKIE' not in os.environ:
    print "Content-type:applicaion/json"
    print
    dump_response_and_exit(False, 'The cookie was not set or has expired.')


cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SmartCookie()
cookie.load(cookie_string)
if '_yagra_session' in cookie:
    cookie['_yagra_session']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

print cookie
print "Content-type:applicaion/json"
print

try:
    con = connect_db()
    session_id = cookie['_yagra_session'].value
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM `Session` WHERE id = %s", (session_id,))
        con.commit()
    dump_response_and_exit(True, "Logout successfully.")
except KeyError:
    dump_response_and_exit(False, 'The cookie was not set or has expired.')
except Error, e:
    if con:
        con.rollback()
    dump_response_and_exit(False, e[1])
finally:
    con.close()

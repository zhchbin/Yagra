#!/usr/bin/python
# -*- coding: utf-8 -*-

from util import connect_db, dump_response_and_exit
from MySQLdb import Error

import Cookie
import cgi
import hashlib
import uuid
import time

cookie = Cookie.SmartCookie()
session_id = uuid.uuid1().get_hex()
cookie['_yagra_session'] = session_id
cookie['_yagra_session']['expires'] = 'Session'
cookie['_yagra_session']['HttpOnly'] = True

print cookie
print "Content-type:applicaion/json"
print
form = cgi.FieldStorage()
username = form.getvalue('username')
password = form.getvalue('password')

if username is None or password is None:
    dump_response_and_exit(False, '请输入用户名和密码。')

try:
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT password FROM User WHERE username=%s", (username,))
        data = cur.fetchall()
        if (len(data) == 0) or data[0][0] != hashlib.sha1(password).digest():
            dump_response_and_exit(False, "用户名或密码错误。")

        # Store cookie id into database.
        #
        # SQL for IF EXISTS UPDATE ELSE INSERT INTO,
        # See http://stackoverflow.com/questions/15383852.
        cur.execute("""INSERT INTO Session
                        (id, username, createAt)
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE
                        id = VALUES(id),
                        createAt = VALUES(createAt)""",
                    (session_id, username, time.strftime('%Y-%m-%d %H:%M:%S')))
        con.commit()
        dump_response_and_exit(True, "Login successfully.")
except Error, e:
    if con:
        con.rollback()
    dump_response_and_exit(False, e[1])
finally:
    con.close()

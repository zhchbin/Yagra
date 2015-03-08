#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import USER_AVATAR_DIRECTORY
from hashlib import md5
from util import connect_db, dump_response_and_exit, forbidden
from MySQLdb import Error

import Cookie
import cgi
import os
import sys

if 'HTTP_COOKIE' not in os.environ:
    forbidden()

cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SmartCookie()
cookie.load(cookie_string)
if '_yagra_session' not in cookie:
    forbidden()

print "Content-type:applicaion/json"
print

session_id = cookie['_yagra_session'].value
con = connect_db()
try:
    cur = con.cursor()
    cur.execute("SELECT username FROM Session WHERE id=%s", (session_id,))
    data = cur.fetchall()
    if len(data) == 0:
        dump_response_and_exit(False, '非法会话，请重新登陆。')
    username = data[0]
except Error, e:
    dump_response_and_exit(False, e[1])

if not os.path.exists(USER_AVATAR_DIRECTORY):
    os.makedirs(USER_AVATAR_DIRECTORY)

form = cgi.FieldStorage()
if 'filename' not in form or not form['filename'].filename:
    dump_response_and_exit(False, '请选择文件。')

fn = os.path.basename(form['filename'].filename)
suffix = fn.split('.')[-1].lower()
if suffix not in ['bmp', 'jpeg', 'jpg', 'png', 'gif', 'webp']:
    dump_response_and_exit(False, '不合法的文件。')

image = form['filename'].file.read()
image_md5 = md5(image).hexdigest()
image_filename = image_md5 + '.' + suffix
with open(USER_AVATAR_DIRECTORY + image_filename, 'wb') as f:
    f.write(image)

try:
    cur = con.cursor()
    cur.execute("""
        UPDATE User
        SET avatar=%s
        WHERE username=%s
    """, (image_filename, username))
    con.commit()
except Error, e:
    dump_response_and_exit(False, e[1])
finally:
    con.close()

message = 'Your avatar "' + fn + '" was uploaded successfully.'
dump_response_and_exit(True, message)

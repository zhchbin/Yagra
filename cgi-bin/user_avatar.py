#!/usr/bin/python

from config import USER_AVATAR_DIRECTORY
from util import print_html_and_exit, connect_db
from MySQLdb import Error

import cgi
import mimetypes

form = cgi.FieldStorage()
username = form.getvalue('username')

try:
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT avatar FROM User WHERE username=%s", (username,))
    data = cur.fetchall()
    if len(data) == 0:
        print_html_and_exit('Invalid username.')
    avatar = data[0][0]
    suffix = avatar.split('.')[-1].lower()
    avatar = USER_AVATAR_DIRECTORY + '/' + avatar
    mimetypes.init()
    with open(avatar, 'r') as f:
        print "Content-type: " + mimetypes.types_map['.' + suffix] + '\n'
        print f.read()
except Error, e:
    print_html_and_exit(e[1])
finally:
    con.close()

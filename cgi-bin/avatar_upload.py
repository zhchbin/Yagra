#!/usr/bin/python

from config import USER_AVATAR_DIRECTORY
from hashlib import md5
from util import connect_db
from MySQLdb import Error

import Cookie
import cgi
import os
import sys


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
        print_html_and_exit('Invalid session.')
    username = data[0]
except Error, e:
    print_html_and_exit(e[1])

if not os.path.exists(USER_AVATAR_DIRECTORY):
    os.makedirs(USER_AVATAR_DIRECTORY)

form = cgi.FieldStorage()
if 'filename' not in form or not form['filename'].filename:
    print_html_and_exit('No file was uploaded.')

fn = os.path.basename(form['filename'].filename)
suffix = fn.split('.')[-1].lower()
if suffix not in ['bmp', 'jpeg', 'jpg', 'png', 'gif', 'webp']:
    print_html_and_exit('Invalid image format.')

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
    print_html_and_exit(e[1])
finally:
    con.close()

message = 'Your avatar "' + fn + '" was uploaded successfully.'
print_html_and_exit(message)

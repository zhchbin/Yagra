#!/usr/bin/python

from hashlib import sha1

import hmac
import json
import os
import subprocess
import sys


# Due to |hmac.compare_digest| is new in python 2.7.7, in order to be
# compatible with other 2.7.x version, we use a similar implementation of
# |compare_digest| to the Python implementation.
#
# See: http://stackoverflow.com/questions/18168819
def compare_digest(x, y):
    if not (isinstance(x, bytes) and isinstance(y, bytes)):
        raise TypeError("both inputs should be instances of bytes")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= int(a, 16) ^ int(b, 16)
    return result == 0


def verify_signature(payload_body):
    x_hub_signature = os.getenv("HTTP_X_HUB_SIGNATURE")
    if not x_hub_signature:
        return False

    sha_name, signature = x_hub_signature.split('=')
    if sha_name != 'sha1':
        return False

    # Never hardcode the token into real product, but now we are finishing
    # homework.
    SECRET_TOKEN = 'nQLr1TFpNvheiPPw9FnsUYD8vSeEV79L'
    mac = hmac.new(SECRET_TOKEN, msg=payload_body, digestmod=sha1)
    return compare_digest(mac.hexdigest(), signature)


print 'Content-Type: application/json\n\n'
result = {}
event = os.getenv('HTTP_X_GITHUB_EVENT')
if event != 'push':
    result['success'] = False
else:
    payload_body = sys.stdin.read()
    result['success'] = verify_signature(payload_body)
    if result['success']:
        path = os.path.dirname(os.path.realpath(__file__))
        process = subprocess.Popen('git pull && git submodule update',
                                   cwd=path,
                                   shell=True)

print json.dumps(result)

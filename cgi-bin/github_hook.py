#!/usr/bin/python

from hashlib import sha1

import hmac
import json
import os
import subprocess
import sys


import cgitb; cgitb.enable()

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
    return hmac.compare_digest(mac.hexdigest(), signature)

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

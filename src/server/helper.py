import os, json
import jwt
from flask import request
from .helper_ldap3 import *

def encode_ldap_auth_token(cred, secret="secret", algorithm="HS256"):
    return jwt.encode(cred, secret, algorithm=algorithm)

def decode_ldap_auth_token(token, secret="secret", algorithm="HS256"):
    return jwt.decode(token, secret, algorithm=algorithm)

def get_config():
    from .config import config
    return config

def get_request_paged_params():
    default = { "size": 10, "page": 0 }
    for k in default.keys():
        if request.args.__contains__(k):
            default[k] = int(request.args[k])
    return default

def request_is_json():
    return request.headers['content-type'] == 'application/json'

def get_request_token():
    return request.headers['x-auth-token']

def gen_auth_token(cred, config):
    return bytes.decode(encode_ldap_auth_token(cred))

def load_data(filename):
    with open(filename, 'r') as f:
        return f.read()

def load_json(filename):
    return json.loads(load_data(filename))

def get_helper(cred_or_token, config):
    cred = None
    if not type(cred_or_token) == dict:
        token = str(cred_or_token)
        cred = decode_ldap_auth_token(token)
    else:
        cred = cred_or_token
    uid = cred.__contains__("username") and cred['username']
    pwd = cred.__contains__("password") and cred['password']
    user_basedn = get_ldap_user_basedn(uid, config)
    return get_ldap_helper(config, basedn=user_basedn, passwd=pwd)

def do_request(callback, helper):
    ret = None
    if helper['bind']():
        ret = callback(helper)
        helper['unbind']()
    return ret

def do_search(helper, basedn, filter, **kwargs):
    def handler(helper):
        results = []
        for entry in helper['search'](basedn, filter, **kwargs):
            results.append(json.loads(entry.entry_to_json()))
        return results
    return do_request(handler, helper)

from flask import Blueprint, request, jsonify
import os, json
from .helper import *

api = Blueprint('api', __name__)

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

@api.route("/users", methods=["GET"])
def get_all_users():
    token = get_request_token()
    config = get_config()
    page = get_request_paged_params()
    if token:
        helper = get_helper(token, config)
        bdn = config["ldap.user.basedn"]
        dn  = bdn[(bdn.find(",")+1):]
        q   = "(uid=*)"
        scope  = "sub"
        limit = page["size"]
        results = do_search(helper, dn, q, \
            scope=scope, limit=limit)
        if results:
            return jsonify(results), 200
        else:
            return "", 404
    return "", 403

@api.route("/user/<uid>", methods=["GET"])
def get_one_user(uid):
    token = get_request_token()
    config = get_config()
    if token:
        helper = get_helper(token, config)
        dn = config["ldap.user.basedn"] % uid
        q  = "(uid=*)"
        scope  = "base"
        results = do_search(helper, dn, q, \
            scope=scope)
        if results and len(results) > 0:
            return jsonify(results[0]), 200
        else:
            return "", 404
    return "", 403


@api.route("/auth", methods=["POST"])
def post_auth():
    if request_is_json():
        cred = request.get_json()
        config = get_config()
        helper = get_helper(cred, config)
        def handler(helper):
            who = helper['whoami']()
            return { "who": who, "token": gen_auth_token(cred, config) }
        ret = do_request(handler, helper)
        return jsonify(ret), 202
    return "", 403

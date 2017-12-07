from flask import Blueprint, request, jsonify
import os, json
from .helper import *

api = Blueprint('api', __name__)

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

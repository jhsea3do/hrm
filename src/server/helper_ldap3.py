import sys, ldap3

def get_ldap_user_basedn(uid, config):
    if "admin" == uid:
        return config['ldap.admin.basedn']
    basedn = config['ldap.user.basedn'] % uid
    return basedn

def get_ldap_conn(server, config, basedn=None, passwd=None):
    basedn = basedn or config['ldap.admin.basedn']
    passwd = passwd or config['ldap.admin.passwd']
    conn = ldap3.Connection(server, user=basedn, password=passwd, \
         auto_bind=False, lazy=False, raise_exceptions=True)
    return conn

def get_ldap_whoami(conn, config):
    return conn.extend.standard.who_am_i()

def get_ldap_search_scope(scope):
    if "sub" == scope:
        return ldap3.SUBTREE
    elif "base" == scope:
        return ldap3.BASE
    else:
        return ldap3.LEVEL

def get_ldap_helper(config, basedn=None, passwd=None):
    ldap_host = config['ldap.host']
    ldap_port = config['ldap.port']
    server = ldap3.Server(ldap_host, port=int(ldap_port), get_info=ldap3.ALL)
    conn = get_ldap_conn(server, config, basedn=basedn, passwd=passwd)
    def bind():
        return conn.bind()
    def unbind():
        return conn.unbind()
    def whoami():
        return conn.extend.standard.who_am_i()
    def search(basedn, filter, scope="sub", attrs=["*"], limit=10):
        if conn.search(
            search_base = basedn,
            search_filter = filter,
            search_scope = get_ldap_search_scope(scope),
            attributes = attrs,
            paged_size = limit,
        ):
            return conn.entries
        else:
            return None
    def get_uid():
        return basedn
    def get_pwd():
        return passwd
    return {
        "get_uid": get_uid,
        "get_pwd": get_pwd,
        "bind": bind,
        "unbind": unbind,
        "search": search,
        "whoami": whoami,
    }

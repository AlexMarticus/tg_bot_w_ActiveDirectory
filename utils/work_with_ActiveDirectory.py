from flask import json
from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, ALL
from data.config import LDAP_HOST, LDAP_PORT, LDAP_USER, LDAP_PASSWORD, LDAP_BASE_DN


def find_ad_users(username, phone):
    search_filter = "(&(displayName={0})(phone={1}))"
    with ldap_connection() as c:
        c.search(search_base=LDAP_BASE_DN,
                 search_filter=search_filter.format(username, phone),
                 search_scope=SUBTREE,
                 attributes=ALL_ATTRIBUTES,
                 get_operational_attributes=True)
    try:
        a = c.entries[0]
        return json.loads(c.response_to_json())
    except:
        return 'User cannot be found'


def ldap_connection():
    server = ldap_server()
    return Connection(server, user=LDAP_USER,
                      password=LDAP_PASSWORD)


def ldap_server():
    return Server(host=LDAP_HOST, port=LDAP_PORT, get_info=ALL)

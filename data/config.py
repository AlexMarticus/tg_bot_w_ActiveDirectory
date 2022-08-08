from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

LDAP_HOST = env.str("LDAP_HOST")
LDAP_PORT = env.int("LDAP_PORT")
LDAP_USER = env.str("LDAP_USER")
LDAP_PASSWORD = env.str("LDAP_PASSWORD")
LDAP_BASE_DN = env.str('LDAP_BASE_DN')

DB_NAME = env.str('DB_NAME')
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")

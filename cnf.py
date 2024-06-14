import configparser as cfp
import os

if not os.environ.get( 'TOOLFORGE' ):
    cnf_path = './replica.my.cnf'
else:
    cnf_path = '~/replica.my.cnf'

def load_cnf():
    cnf = cfp.ConfigParser()
    cnf.read(cnf_path)
    return cnf

cnf = load_cnf()

if not os.environ.get( 'TOOLFORGE' ):
    remote = 'localhost'
    user = cnf['client']['user']
    password = cnf['client']['password']
    port=3308
else:
    remote = 'enwiki.analytics.db.svc.wikimedia.cloud'
    user = os.environ.get( 'TOOL_TOOLSDB_USER' )
    password = os.environ.get( 'TOOL_TOOLSDB_PASSWORD' )
    port =3306


config = {
    'host': remote,
    'username': user,
    'password': password,
    'port': port
}
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
user = cnf['client']['user']
password = cnf['client']['password']

if not os.environ.get( 'TOOLFORGE' ):
    remote = 'localhost'
    port=3308
else:
    remote = 'enwiki.analytics.db.svc.wikimedia.cloud'
    port =3306


config = {
    'host': remote,
    'username': user,
    'password': password,
    'port': port
}
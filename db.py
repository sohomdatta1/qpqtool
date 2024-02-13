import pymysql as sql
from cnf import config
    
def get_conn():
    dbconn = sql.connections.Connection(user=config['username'], password=config['password'], port=config['port'], host=config['host'], database='enwiki_p')
    return dbconn

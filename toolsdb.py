import pymysql as sql
from cnf import config
import os

def delete_all_data_do_not_use_in_prod():
    if os.environ.get( 'TOOLFORGE' ):
        raise f'This seems like a production system, please refrain from resetting the database'
    with get_conn().cursor() as cursor:
        cursor.execute('DROP TABLE noms;')

def init_db():
    initdbconn = sql.connections.Connection(user=config['username'], password=config['password'], host='tools.db.svc.wikimedia.cloud')
    with initdbconn.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config["username"]}__qpqtool_p;')
        cursor.execute(f'USE {config["username"]}__qpqtool_p')
        cursor.execute('''CREATE TABLE IF NOT EXISTS `noms` (
                    rev_actor INT,
                    page_title VARCHAR(255),
                    rev_timestamp TIMESTAMP,
                    PRIMARY KEY (rev_actor, page_title)
                    );''')
        cursor.execute('CREATE INDEX rev_actor_index ON noms(rev_actor);')
        cursor.execute('CREATE INDEX page_title_index ON noms(page_title);')
        cursor.execute('CREATE INDEX rev_timestamp_index ON noms(rev_timestamp);')
        cursor.execute('CREATE INDEX rev_actor_page_title_index ON noms(rev_actor, page_title);')
        cursor.execute('CREATE TABLE IF NOT EXISTS `last_run` (job_name VARCHAR(255), last_updated TIMESTAMP);')
    initdbconn.close()
    
def get_conn():
    init_db()
    dbconn = sql.connections.Connection(user=config['username'], password=config['password'], host='tools.db.svc.wikimedia.cloud', database=f'{config["username"]}__qpqtool_p')
    return dbconn

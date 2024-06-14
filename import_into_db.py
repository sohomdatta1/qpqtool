from replicadb import get_conn as get_replica_conn
from toolsdb import get_conn as get_tools_conn

def import_into_db():
    time_offset = 0
    with get_tools_conn().cursor() as cursor:
        cursor.execute('SELECT * FROM last_run WHERE job_name = "import_into_db"')
        last_run = cursor.fetchone()
        if last_run:
            time_offset = last_run[1]
    with get_replica_conn().cursor() as cursor:
        cursor.execute("""SELECT p.page_title, r.rev_actor, r.rev_timestamp
        FROM page p 
        JOIN revision r ON p.page_id = r.rev_page
        AND p.page_namespace = 10
        AND r.rev_timestamp > %s
        AND r.rev_parent_id = '0'
        AND p.page_is_redirect = '0'
        AND p.page_title LIKE 'Did_you_know_nominations/%'
        ORDER BY r.rev_timestamp
        """, (time_offset))
        pages = cursor.fetchall()
        with get_tools_conn().cursor() as tools_cursor:
            for page in pages:
                print('Adding to DB', page)
                tools_cursor.execute('INSERT IGNORE INTO noms (page_title, rev_actor, rev_timestamp) VALUES (%s, %s, %s)', page)
            tools_cursor.execute('REPLACE INTO last_run (job_name, last_updated) VALUES ("import_into_db", NOW())')
            tools_cursor.execute('COMMIT')
        return 'Imported ' + str(len(pages)) + ' rows'

if __name__ == '__main__':
    print(import_into_db())
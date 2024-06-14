from flask import Flask, redirect, send_file
from replicadb import get_conn as get_replica_conn
from toolsdb import get_conn as get_toolsdb_conn
from bleach import clean
import json
from datetime import datetime, timedelta
import re
from redis_init import get_redis_conn, REDIS_KEY_PREFIX

app = Flask(__name__)

@app.get('/')
def main():
    return redirect('/dyk')

@app.get('/dyk')
def dyk():
    return send_file('./index.html')

@app.get('/qpq/<path:username>')
def qpq( username: str ):
    username = username.replace('_', ' ')
    with get_toolsdb_conn().cursor() as toolsdbcursor:
        with get_replica_conn().cursor() as replicacursor:
            replicacursor.execute('SELECT * FROM actor WHERE actor_name = %s;', username)
            actor = replicacursor.fetchone()
            toolsdbcursor.execute('SELECT page_title FROM noms WHERE rev_actor = %s;', actor[0])
            pages = toolsdbcursor.fetchall()
            resp_json = []
            for page in pages:
                resp_json.append('Template:' + page[0].decode())
            if len(resp_json) == 0:
                return '<h1>No DYK nominations found</h1>'
            
            list_html = []
            for page in resp_json:
                list_html.append( f'<li><a href="https://en.wikipedia.org/wiki/{page}" target="_blank">{page}</a></li>')
            listofdyknoms = '<ol>' + '\n'.join(list_html) + '</ol>'

            if len(resp_json) < 5:
                return '<h1> Less than 5 DYK nominations found</h1>\n' + listofdyknoms
            
            return f'<h1>QPQ required, these are all of {clean(username)}\'s DYK noms</h1>' + listofdyknoms
        
@app.get('/credits/<path:username>')
def credits(username):
    username = username.replace(' ', '_')
    resp_json = []
    with get_conn().cursor() as cursor:
        cursor.execute("""SELECT c.comment_text
        FROM page p 
        JOIN revision r ON p.page_id = r.rev_page
        JOIN comment c ON r.rev_comment_id = c.comment_id
        AND p.page_namespace = 3
        AND p.page_title = %s
        AND r.rev_actor = 24447
        ORDER BY r.rev_timestamp;
        """, (username))
        comments = cursor.fetchall()
        for comment in comments:
            try:
                page = re.search(r'Giving DYK credit for \[\[([^\]]+)\]\] on behalf of \[\[([^\]]+)\]\]', comment[0].decode()).groups()[0]
                resp_json.append(page)
            except Exception as _:
                print(_)
                pass
        
        if len(resp_json) == 0:
            return '<h1>No DYK nominations found</h1>'
        
        list_html = []
        for page in resp_json:
            list_html.append( f'<li>At <a href="https://en.wikipedia.org/wiki/Template:Did_you_know_nominations/{page}" target="_blank">Template:Did you know nominations/{page}</a> ' + 
                                f'for <a href="https://en.wikipedia.org/wiki/{page}" target="_blank">{page}</a></li>')
        listofdyknoms = '<ol>' + '\n'.join(list_html) + '</ol>'
        
        return f'<h1>DYK credits given to {clean(username)}</h1>' + listofdyknoms

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
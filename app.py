from flask import Flask
from db import get_conn
from bleach import clean
import json
from datetime import datetime, timedelta
from redis_init import rediscl as r, REDIS_KEY_PREFIX

app = Flask(__name__)

@app.get('/qpq/<path:username>')
def qpq( username: str ):
    cached_val = r.get(REDIS_KEY_PREFIX + username)
    if cached_val == None:
        offset = 0
        cached_response = []
    else:
        offset = int(cached_val.split(b'|', 1)[0])
        cached_response = json.loads( cached_val.split(b'|',1)[1] )
    with get_conn().cursor() as cursor:
        cursor.execute("""SELECT p.page_title
        FROM page p 
        JOIN revision r ON p.page_id = r.rev_page
        AND p.page_namespace = 10
        AND r.rev_timestamp > %s
        AND r.rev_parent_id = '0'
        AND p.page_is_redirect = '0'
        AND r.rev_actor IN (SELECT actor_id FROM actor WHERE actor_name = %s)
        AND p.page_title LIKE %s
        GROUP BY page_title
        """, (int(offset), username, 'Did_you_know_nominations/%'))
        pages = cursor.fetchall()
        print(len(pages))
        resp_json = cached_response
        for page in pages:
            resp_json.append('Template:' + page[0].decode())
        tmstmp = datetime.now().strftime("%Y%m%d%H%M%S")
        r.set(REDIS_KEY_PREFIX + username, tmstmp + '|' + json.dumps(resp_json))
        r.expire(REDIS_KEY_PREFIX + username, timedelta(days=365 * 2))
        if len(resp_json) == 0:
            return '<h1>No DYK nominations found</h1>'
        
        list_html = []
        for page in resp_json:
            list_html.append( f'<li><a href="https://en.wikipedia.org/wiki/{page}" target="_blank">{page}</a></li>')
        listofdyknoms = '<ol>' + '\n'.join(list_html) + '</ol>'

        if len(resp_json) < 5:
            return '<h1> Less than 5 DYK nominations found</h1>\n' + listofdyknoms
        
        return f'<h1>QPQ required, these are all of {clean(username)}\'s DYK noms</h1>' + listofdyknoms

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
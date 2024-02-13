from flask import Flask
from db import get_conn
from bleach import clean

app = Flask(__name__)

@app.get('/qpq/<path:username>')
def qpq( username: str ):
    with get_conn().cursor() as cursor:
        cursor.execute("""SELECT p.page_title
        FROM page p 
        JOIN revision r ON p.page_id = r.rev_page
        AND p.page_namespace = 10
        AND r.rev_parent_id = '0'
        AND p.page_is_redirect = '0'
        AND r.rev_actor IN (SELECT actor_id FROM actor WHERE actor_name = %s)
        AND p.page_title LIKE %s
        GROUP BY page_title
        """, (username, 'Did_you_know_nominations/%'))
        pages = cursor.fetchall()
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
        else:
            return f'<h1>QPQ required, these are all of {clean(username)}\'s DYK noms</h1>' + listofdyknoms

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
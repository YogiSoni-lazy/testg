import json
import sqlite3
from flask import abort, Flask, g, make_response, request

app = Flask(__name__)

DATABASE = './data/reporting.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def get_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def open_db_connection():
    g.db = connect_db()


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/v1/healthz', methods=['GET'])
def healthz():
    return {'health': 'ok'}


@app.route('/v1/report', methods=['POST'])
def post_log():
    if not request.is_json:
        abort(400)

    connection = get_connection()
    c = connection.cursor()

    c.execute('INSERT INTO reports VALUES (?)', [json.dumps(request.json)])

    connection.commit()
    connection.close()

    response = make_response('')
    response.headers['Location'] = '/v1/report/{}'.format(c.lastrowid)

    return response, 201


@app.route('/v1/report/<int:id>', methods=['GET'])
def get_log(id):

    log = query_db('SELECT * FROM reports WHERE ROWID = ?', [id], one=True)

    if log is None:
        abort(404)

    return json.loads(log.get('record'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

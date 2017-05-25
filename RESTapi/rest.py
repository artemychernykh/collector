import flask
import os
import psycopg2
from urllib.parse import urlparse

def make_connection():
    postgresql_url = os.getenv('POSTGRESQL_PORT')
    postgresql_url = urlparse(postgresql_url)
    HOST = postgresql_url.hostname
    PORT = postgresql_url.port
    con = psycopg2.connect(dbname='news', user='postgres', password='postgres', host=HOST, port=PORT)
    cur = con.cursor()
    return con, cur


def take_db(con, cur):
    command = "SELECT * FROM news"
    cur.execute(command)
    con.commit()
    lst_news = cur.fetchall()
    return lst_news


app = flask.Flask(__name__)

  
@app.route('/index')
def dwnld_html():
    con, cur = make_connection()
    records = take_db(con, cur)
    con.close()
    return flask.render_template('index.html', records=records)
    return flask.send_file('news.html')


if __name__ == '__main__':
    app.run(debug = True)

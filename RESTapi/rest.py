import flask
import os
from urllib.parse import urlparse
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase


postgresql_url = os.getenv('POSTGRESQL_PORT')
postgresql_url = urlparse(postgresql_url)
host = postgresql_url.hostname
port = postgresql_url.port
    
db = PostgresqlExtDatabase(
     'news',
     user='postgres',
     password='postgres',
     host=host, 
     port=port,
     register_hstore=False)

class News(Model):
    site = CharField(max_length=255)
    title = CharField(max_length=1500)
    description = CharField(max_length=5000)
    article = CharField(null=True, max_length=50000)
    date_news = DateTimeField()
    link = CharField(unique=True)
    class Meta:
        database = db
        

app = flask.Flask(__name__)

  
@app.route('/index')
def index():
    
    records = News.select()
    sites = list(map(lambda x: x.site, News.select(News.site).distinct()))
    return flask.render_template('index.html', records=records, sites=sites)


@app.route('/search=<word>')
def search(word):
    return word
    
if __name__ == '__main__':
    app.run(debug = True)

import flask
import os
from urllib.parse import urlparse
from peewee import *
from playhouse.postgres_ext import *

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
    site = TextField()
    title = TextField()
    description = TextField()
    article = TextField(null=True)
    date_news = DateTimeField()
    link = TextField(unique=True)
    id = IntegerField(null=True,  index=True)
    search_content = TSVectorField(null=True)
    class Meta:
        database = db
         

app = flask.Flask(__name__)

  
@app.route('/')
@app.route('/index')
def dwnld_html():
    records = News.select().order_by(News.date_news.desc())
    sites = list(map(lambda x: x.site, News.select(News.site).distinct()))
    return flask.render_template('index.html', records=records, sites=sites)


@app.route('/search=<word>')
def search(word):
    records = (News
                .select()
                .order_by(News.date_news.desc())
                .where(News.search_content.match(word)))
    return flask.render_template('search.html', records=records)
    
    
if __name__ == '__main__':
    app.run()

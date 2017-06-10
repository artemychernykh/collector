from urllib.request import urlopen
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import time
import sys
import os
from tasks import take_article
from peewee import *
from playhouse.postgres_ext import *

time.sleep(5)


list_rss = ["https://russian.rt.com/rss", "https://meduza.io/rss/news",  \
"https://lenta.ru/rss", "http://tass.ru/rss/v2.xml", \
"http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss"]
list_sites = ["rt", "meduza", "lenta", "tass", "rbc"]
N_sites = len(list_sites)
HOUR = 3600
LIMIT = 300

postgresql_url = os.getenv('POSTGRESQL_PORT')
postgresql_url = urlparse(postgresql_url)
HOST = postgresql_url.hostname
PORT = postgresql_url.port

db = PostgresqlExtDatabase(
     'news',
     user='postgres',
     password='postgres',
     host=HOST, 
     port=PORT,
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
        

if not News.table_exists():
    News.create_table()
    

def download_xml(link):
    print(link)
    current = urlopen(link)
    xml = current.readall()
    temfile = open("temfile.xml", 'wb')
    temfile.write(xml)
    temfile.close()


def parsing():
    
    tasks = []
    Number_news = len(News.select())
    for i in range(N_sites):
        current_site = list_sites[i]
        current_url = list_rss[i]
        download_xml(current_url)
        tree = ET.parse("temfile.xml")
        root = tree.getroot()
        i = 0
        #parse
        for item in root.iter('item'):
            if i == LIMIT:
                break
            i += 1
            link = item.find('guid')
            if len(News.select().where(News.link==link.text)):
                continue
            title = item.find('title')
            description = item.find('description')
            date = item.find('pubDate')
            Number_news += 1
            id = Number_news
            task = take_article.delay(current_site, link.text)
            tasks.append({'article': task, 'link': link.text})
            if description is not None:
                desc = description.text
            else:
                desc = ''
            News.create(
                site=current_site, 
                title=title.text, 
                description=desc,
                date_news=date.text, 
                link=link.text, 
                id=id)
   # добавляет текст статьи 
    while True:
        complete_tasks = list(filter(lambda x: x['article'].ready(), tasks))
        tasks = list(filter(lambda x: x not in complete_tasks, tasks))
        for task in complete_tasks:
            News.update(article=task['article'].get()).where(News.link==task['link']).execute()
            record = News.select().where(News.link==task['link'])[0]
            News.update(
                search_content=fn.to_tsvector(
                str(record.title)+str(record.description)+str(record.article))
                ).where(News.link==task['link']).execute()
        if not tasks:
            break
        time.sleep(1)
        
    print('done')


def inf_parse():
    while True:
        parsing()
        time.sleep(2*HOUR)

  
if len(sys.argv) == 2 and sys.argv[1] == 'inf':
    inf_parse()
else:
    parsing()
    

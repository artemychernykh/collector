import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.parse import urlparse
import psycopg2
import time
import sys
import os
from tasks import take_article

time.sleep(10)

postgresql_url = os.getenv('POSTGRESQL_PORT')
postgresql_url = urlparse(postgresql_url)
HOST = postgresql_url.hostname
PORT = postgresql_url.port

list_rss = ["https://russian.rt.com/rss", "https://meduza.io/rss/news",  \
"https://lenta.ru/rss", "http://tass.ru/rss/v2.xml", \
"http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss"]
list_sites = ["RT", "meduza", "lenta.ru", "tass",  "rbc"]
N_sites = len(list_sites)
HOUR = 3600
LIMIT = 300


def create(con, cur):
    command = "CREATE TABLE news(site varchar(40), title varchar(400),\
    description varchar(1500), article varchar(50000), date_news date, link varchar(200) UNIQUE)"
    cur.execute(command)
    con.commit() 

con = psycopg2.connect(dbname='news', user='postgres', password='postgres', host=HOST, port=PORT)
cur = con.cursor()


try:
    create(con, cur)
except:
    con.commit()


command = "DELETE FROM news"
cur.execute(command)
con.commit()    
    
def screening(mess):
        mess = mess.replace('«', '"')
        mess = mess.replace('»', '"')
        return mess.replace("'",  "''")


def add(site, title, description, date,  link): # to db
    desc = screening(description)
    title = screening(title)
    command = "INSERT INTO news(site,title,description, date_news, link)\
    VALUES('{}','{}','{}','{}','{}')".format(site, title, desc, date, link)
    cur.execute(command)
    con.commit()


def add_article(article, link): 
    article = screening(article)
    command = "UPDATE news SET article='{}' WHERE link='{}'".format(article, link)
    cur.execute(command)
    con.commit()


def download_xml(link):
    print(link)
    current = urlopen(link)
    xml = current.readall()
    temfile = open("temfile.xml", 'wb')
    temfile.write(xml)
    temfile.close()

def parsing():
    
    tasks = []
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
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            date = item.find('pubDate')
            print(link.text )
            # здесь проверка
            task = take_article.delay(current_site, link.text)
            tasks.append({'article': task, 'link': link.text})
            
            if description is not None:
                desc = description.text
            else:
                desc = ''
            try:
                add(current_site,  title.text,  desc,  date.text,  link.text)
            except:
                con.commit()
    
    # добавляет текст статьи 
    while True:
        complete_tasks = list(filter(lambda x: x['article'].ready(), tasks))
        tasks = list(filter(lambda x: x not in complete_tasks, tasks))
        for task in complete_tasks:
            add_article(task['article'].get(), task['link'])
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
    

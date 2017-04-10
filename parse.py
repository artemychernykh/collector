import xml.etree.ElementTree as ET
from urllib.request import urlopen
import psycopg2
import time
import sys
import parse_article as pa

list_rss = ["https://russian.rt.com/rss", "https://meduza.io/rss/news",  \
"https://lenta.ru/rss", "http://tass.ru/rss/v2.xml", \
"http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss"]

list_sites = ["RT", "meduza", "lenta.ru", "tass",  "rbc"]

N_sites = len(list_sites)

HOUR = 3600
LIMIT = 3

def create():
    command = "CREATE TABLE news(site varchar(40), title varchar(400),\
    description varchar(1500), article varchar(50000), date_news date, link varchar(200) UNIQUE)"
    cur.execute(command)
    con.commit() 

con = psycopg2.connect(dbname='news', user='postgres',  host='postgresql')
cur = con.cursor()

try:
    create()
except:
    pass
    
    
def screening(mess):
        mess = mess.replace('«', '"')
        mess = mess.replace('»', '"')
        return mess.replace("'",  "''")
        

def add(site, title, description, date,  link, article): # to db
    desc = screening(description)
    title = screening(title)
    article = screening(article)
    command = "INSERT INTO news(site,title,description, date_news, link, article)\
    VALUES('{}','{}','{}','{}','{}','{}')".format(site, title, desc, date, link, article)
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
            print(link.text)
            article = pa.take_article(current_site, link.text)
            
            if description is not None:
                desc = description.text
            else:
                desc = ""
            try:
                add(current_site,  title.text,  desc,  date.text,  link.text,  article)
            except:
                pass
            
        print('done')


def inf_parse():
    while True:
        parsing()
        time.sleep(2*HOUR)
    
if len(sys.argv) == 2 and sys.argv[1] == 'inf':
    inf_parse()
else:
    parsing()
    

from bs4 import BeautifulSoup
from urllib.request import urlopen
from celery import Celery
import requests

app = Celery('task')
app.config_from_object('setting')


def write(strr): # delete
    file = open('123.txt', 'a')
    file.write(str(strr) + '\n')
    file.close()
    
    
def take_page(link):
    #page = urlopen(link).readall()
    page = requests.get(link).text
    return BeautifulSoup(page,  'html.parser')


def paragraph_parse(article):
    rez = ''
    for par in article.find_all('p'):
        rez += ''.join(par.strings)
    return rez


def take_div(page, name_par): # когда внутри только текст( нет div и p)
    rez = page.find('div', name_par)
    return rez.string if rez else ''
 

def take_paragraphs(page, article_class):
    article_text = page.find('div', article_class)
    return paragraph_parse(article_text) if article_text else ''
 
def parse_rt(page):
    article_text = page.find('div', 'article__text')
    rez = take_div(page, 'article__summary') +\
    paragraph_parse(article_text) if article_text else ''
    return rez


def parse_meduza(page):
    return take_paragraphs(page, 'Body')


def parse_lenta(page):
    return take_paragraphs(page, 'b-text')
    

def parse_rbc(page):
    return take_paragraphs(page, 'article__content')

def parse_tass(page):
    return take_paragraphs(page, "b-material-text__l")

@app.task
def take_article(site, link):
    
    page = take_page(link)
        
    sites = {"rt": parse_rt,  "meduza": parse_meduza,  "lenta": parse_lenta,  \
            "tass": parse_tass, "rbc": parse_rbc}
    if site in sites:
        return sites[site](page)
    return ''


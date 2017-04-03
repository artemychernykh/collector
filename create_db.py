import psycopg2
import argparse
import sys

con = psycopg2.connect(dbname='news', user='postgres', host='localhost')
cur = con.cursor()
cur = con.cursor()

def create(args):
    command = "CREATE TABLE news(site varchar(40), title varchar(400),\
    description varchar(1500), article varchar(50000), date_news date, link varchar(200) UNIQUE)"
    cur.execute(command)
    con.commit()
    
def add(args):
    command = "INSERT INTO news(site,title,description,date_news,link)\
    VALUES('www.lenta.ru','умер вождь','сегодня умер',CURRENT_DATE,\
    'lenta.ru/qwer/1')"
    cur.execute(command)
    con.commit()
    
def delete(args):
    print('go')
    command = "DELETE FROM news"
    cur.execute(command)
    con.commit()

def take_db():
    command = "SELECT * FROM news"
    cur.execute(command)
    con.commit()
    lst_news = cur.fetchall()
    return lst_news

def make_html(args):
    print("MAKE")
    newshtml = open("news.html",  "w")
    lst_news = take_db()
    page = u"<html>\n<head>\n<title>бд</title></head>\n<body>\n"
    end_page = u"</table>конец</body></html>"
    tbl = u"<table><tr>"
    newshtml.write(page)
    newshtml.write(tbl)
    i = 0
    for col in lst_news:
        i += 1
        try:
            newshtml.write("<table border='1'><tr>")
            line = ("<td>{}</td>"*4).format(col[0], col[1], col[2], col[4]) + \
                    "<td><a href={}>{}</a></td>".format(col[5], col[5])
            newshtml.write(line + "</tr></table>\n")
            line_article = col[3]
            newshtml.write(line_article) 
        except:
            print(i)
        #pass
    newshtml.write(end_page)
    newshtml.close()
    

def show(args):
    print("show")
    fl = open('news.txt', 'w')
    lst_news = take_db()
    i = 0
    for one_news in lst_news:
        try:
            fl.write(str(one_news))
            fl.write("\n")
            print(one_news)
        except Exception:
           pass
    fl.close()
    

help = "работа с бд, ключи \n create создать таблицу \n delete \
удалить содержимое таблицы \n show показать содержимое таблицы"
parser = argparse.ArgumentParser(usage=help)
subparsers = parser.add_subparsers()

parser_append = subparsers.add_parser("create")
parser_append.set_defaults(func=create)

parser_append = subparsers.add_parser("delete")
parser_append.set_defaults(func=delete)

parser_append = subparsers.add_parser("show")
parser_append.set_defaults(func=show)

parser_append = subparsers.add_parser("add")
parser_append.set_defaults(func=add)

parser_append = subparsers.add_parser("makehtml")
parser_append.set_defaults(func=make_html)



args = parser.parse_args()
if vars(args):
    args.func(args)
else:
    print(help)

con.close()

print('done')

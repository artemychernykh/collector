import flask
import os
import psycopg2
from urllib.parse import urlparse
import json

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

def make_html(con, cur):
    print("MAKE")
    newshtml = open("news.html",  "w")
    lst_news = take_db(con, cur)
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
            pass
    newshtml.write(end_page)
    newshtml.close()


def make_json(con, cur):
    file = open('news.json', 'w')
    list_news  = take_db(con, cur)
    for col in list_news:
            article = {'site': col[0], 'title': col[1], 'description':col[2], \
            'article':col[3], 'date':str(col[4]), 'link':col[5]}
            file.write(json.dumps(article))
            file.write('\n')
            
    file.close()
    


app = flask.Flask(__name__)
    
@app.route('/downloadhtml')
def dwnld_html():
    con, cur = make_connection()
    make_html(con, cur)
    con.close()
    return flask.send_file('news.html')

@app.route('/downloadjson')
def dwnld_json():
    con, cur = make_connection()
    make_json(con, cur)
    con.close()
    return flask.send_file('news.json')


if __name__ == '__main__':
    app.run(debug = True)

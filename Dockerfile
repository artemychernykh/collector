FROM python:3.4
ADD create_db.py parse.py parse_article.py /
RUN pip3 install bs4 requests psycopg2
CMD python3 parse.py

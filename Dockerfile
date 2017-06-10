FROM python:3.4
ADD create_db.py parse.py parse_article/tasks.py parse_article/setting.py /
RUN pip3 install bs4 requests celery redis celery-with-redis peewee psycopg2
CMD python3 parse.py
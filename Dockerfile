FROM python:3.4
ADD create_db.py parse.py parse_article/tasks.py parse_article/setting.py /
RUN pip3 install bs4 requests psycopg2 celery redis celery-with-redis
CMD python3 parse.py

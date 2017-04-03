FROM python:3.4
ADD ./create_db.py / parse.py / parse_article.py /
VOLUME storage
RUN pip3 install bs4
RUN pip3 install requests
RUN pip3 install psycopg2
CMD python3 parse.py

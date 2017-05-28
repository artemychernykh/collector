FROM python:3.4
EXPOSE 5000
RUN mkdir templates
ADD rest.py /
ADD templates/index.html templates/index.html
RUN pip3 install psycopg2 flask uwsgi
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--master", "--module", "rest:app", "--processes", "1", "--threads", "4", "--uid", "nobody", "--gid", "nogroup"]

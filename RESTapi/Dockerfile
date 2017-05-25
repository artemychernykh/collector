FROM python:3.4
EXPOSE 5000
ADD rest.py /
RUN pip3 install psycopg2 flask uwsgi
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--master", "--module", "rest:app", "--processes", "1", "--threads", "4", "--uid", "nobody", "--gid", "nogroup"]

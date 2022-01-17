FROM python:3.7

WORKDIR /srv
ADD ./requirements.txt /srv/requirements.txt
RUN pip3 install -r requirements.txt
ADD . /srv
WORKDIR /srv


ADD /webapi .
CMD gunicorn webapi.wsgi --timeout 3600 --bind 0.0.0.0:8000 -w 4


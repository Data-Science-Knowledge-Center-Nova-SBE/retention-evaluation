FROM python:3.6

WORKDIR /srv
ADD ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
ADD . /srv

CMD gunicorn webapi.wsgi --timeout 3600 --bind 0.0.0.0:8000 -w 4

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
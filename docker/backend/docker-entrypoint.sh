#!/bin/sh

if [ "$*" == "" ]; then
	python3 manage.py makemigrations && \
	python3 manage.py makemigrations main && \
	python3 manage.py migrate && \
	exec uwsgi --master \
			--processes=1 \
			--attach-daemon='celery worker --app=main --concurrency=3 --loglevel=info --logfile=/dev/stderr' \
			--attach-daemon='celery beat --app=main --loglevel=info --logfile=/dev/stderr' \
			--socket /var/run/python/uwsgi.sock \
			--plugins python3 \
			--protocol uwsgi \
			--chmod-socket=666 \
			--die-on-term
else
  exec "$@"
fi

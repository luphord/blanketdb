FROM alpine:3.9

RUN apk add --no-cache \
        uwsgi-python3 \
        python3

EXPOSE 80
VOLUME /usr/src/app/db
WORKDIR /usr/src/app

COPY blanketdb.py blanketdb_wsgi.py ./

CMD [ "uwsgi", "--socket", "0.0.0.0:80", \
               "--plugins", "python3", \
               "--protocol", "http", \
               "--wsgi", "blanketdb_wsgi:application" ]
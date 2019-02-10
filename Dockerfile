FROM alpine:3.9

RUN apk add --no-cache \
        uwsgi-python3 \
        python3

EXPOSE 3031
VOLUME /usr/src/app/db
WORKDIR /usr/src/app

COPY blanketdb.py blanketdb_wsgi.py ./

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi", "blanketdb_wsgi:application" ]
FROM geoneric/nc_base:latest

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY nc_plan /nc_plan
COPY test /test

CMD ["/cmd.sh"]

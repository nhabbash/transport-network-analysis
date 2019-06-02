FROM postgres:latest
ADD ./script/load.sql /docker-entrypoint-initdb.d
COPY ./dataset /tmp/dataset
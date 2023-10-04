FROM postgres:15-bullseye

COPY ./docker/local/postgres/mainteinance /usr/local/bin/mainteinance

RUN chmod +x /usr/local/bin/mainteinance/*

RUN mv /usr/local/bin/mainteinance/* /usr/local/bin \
  && rmdir /usr/local/bin/mainteinance
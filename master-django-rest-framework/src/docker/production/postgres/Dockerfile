FROM postgres:15-bullseye

COPY ./docker/production/postgres/mainteinance /usr/production/bin/mainteinance

RUN chmod +x /usr/production/bin/mainteinance/*

RUN mv /usr/production/bin/mainteinance/* /usr/production/bin \
  && rmdir /usr/production/bin/mainteinance
FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Sent output directly to the terminal within container
ENV PYTHONNONBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . .


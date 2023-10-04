FROM python:3.9
# useful for logs
ENV PYTHONBUFFERED 1 
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
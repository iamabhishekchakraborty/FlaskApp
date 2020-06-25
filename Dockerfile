FROM python:3.6.9
MAINTAINER Abhishek

ENV JENKINS_USER "abhishek"
ENV JENKINS_PASS "admin"
ENV APP_SETTINGS = "config.DevelopmentConfig"
ENV FLASK_RUN_PORT=8000

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE  8000
CMD ["python3", "app.py"]

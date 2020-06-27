FROM python:3.6.4

MAINTAINER Abhishek

ENV JENKINS_USER="abhishek"
ENV JENKINS_PASS="admin"
ENV APP_SETTINGS="config.DevelopmentConfig"
ENV FLASK_RUN_PORT=8000

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Set a health check for the container (for Docker to be able to tell if the server is actually up or not)
HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:8000 || exit 1

# tell docker what port to expose
EXPOSE  8000

CMD ["python3", "app.py"]

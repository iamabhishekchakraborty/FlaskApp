FROM python:3.6.4

MAINTAINER Abhishek

ENV JENKINS_USER="abhishek"
ENV JENKINS_PASS="admin"
ENV APP_SETTINGS="config.DevelopmentConfig"
ENV FLASK_RUN_PORT=8000
ENV FLASK_RUN_HOST 0.0.0.0

RUN mkdir /app
COPY requirements.txt /app/
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app

RUN apt-get update -y && \
    pip install -r requirements.txt

COPY . /app

# Set a health check for the container (for Docker to be able to tell if the server is actually up or not)
HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:8000 || exit 1

# tell docker what port to expose
EXPOSE  8000

CMD ["python3", "app.py"]

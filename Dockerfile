FROM python:3.6.9
MAINTAINER Abhishek

COPY .  /flask_project
WORKDIR /flask_project
RUN pip install -r requirements.txt
EXPOSE  8000
CMD ["python3", "app.py"]

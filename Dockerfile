FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN pip install --upgrade virtualenv
RUN pip install --upgrade setuptools
RUN pip install apache-beam
COPY . /tmp/

WORKDIR /home
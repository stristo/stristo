FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install git python-pip -y
RUN pip install gunicorn
RUN apt-get install couchdb -y

RUN env HOME="/root" && export HOME

WORKDIR /opt
RUN git clone -b dev-0.1 https://github.com/stristo/stristo.git
WORKDIR /opt/stristo

RUN chmod +x run.sh

RUN pip install -r requirements.txt

ENTRYPOINT ./run.sh

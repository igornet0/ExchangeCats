FROM python:latest

RUN apt-get update
RUN apt-get install sudo -y
RUN apt-get install git -y

WORKDIR /var

RUN sudo rm -rf ExchangeCats/

RUN git clone https://github.com/igornet0/ExchangeCats.git
WORKDIR /var/ExchangeCats

RUN pip install --upgrade pip
RUN pip install mysql-connector-python
RUN pip install -r requirements.txt
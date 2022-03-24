FROM python:3.10.3-slim-bullseye

RUN apt update && apt install -y pflogsumm build-essential libssl-dev libffi-dev python-dev

RUN mkdir /breachify

COPY . /breachify/

WORKDIR /breachify
RUN pip3 install -r requirements.txt

ENTRYPOINT python3 /breachify/src/bot.py

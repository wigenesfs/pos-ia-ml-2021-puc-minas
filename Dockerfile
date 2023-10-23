FROM ubuntu:22.04

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY . /app

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 5000
CMD flask run --host 0.0.0.0 --no-reload
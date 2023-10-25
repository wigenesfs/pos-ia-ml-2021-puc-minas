FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt && pip install --upgrade pip

COPY . /app

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
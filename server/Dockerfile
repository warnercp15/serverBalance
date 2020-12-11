FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /code

WORKDIR /code

ADD server.py /code/

ADD const.py /code/

ADD requirements.txt /code/

RUN apk add --no-cache --virtual .build-deps gcc musl-dev 

RUN python -m pip install -r requirements.txt --no-cache-dir

CMD ["python", "server.py"]
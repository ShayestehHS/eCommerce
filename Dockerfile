FROM python:3.9.6-alpine
LABEL MAINTAINER="ShayestehHs"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
# Pillow dependency
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./eCommerce ./app
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
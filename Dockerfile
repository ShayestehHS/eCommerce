FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

ENV PYTHONUNBUFFERED 1

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update postgresql-client

## install psycopg2 dependencies
RUN apk add postgresql-dev python3-dev musl-dev
#
## install Pillow dependencies
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

COPY ./requirements.txt /requirements.txt

RUN apk add --update --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt

COPY ./eCommerce /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
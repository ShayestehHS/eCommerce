FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./eCommerce /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

RUN apk add --update postgresql-client

RUN apk add --update --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers

## install psycopg2 dependencies
RUN apk add postgresql-dev python3-dev musl-dev
#
## install Pillow dependencies
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]

#RUN apk update
#

#
#RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
#RUN pip install -r /requirements.txt
#RUN apk del .tmp
#
#
#COPY ./scripts /scripts
#
#RUN chmod +x /scripts/*
#
#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static
#RUN adduser -D user
##RUN chown -R user:user /vol
##RUN chmod -R 755 /vol/web
#USER user
#
#CMD ["entrypoint.sh"]
FROM python:3.9.6-alpine
LABEL MAINTAINER="ShayestehHS"

RUN apk update

# install psycopg2 dependencies
RUN apk add postgresql-dev python3-dev musl-dev

# install Pillow dependencies
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./eCommerce /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
RUN chmod -R 755 /static
USER user

CMD ["entrypoint.sh"]
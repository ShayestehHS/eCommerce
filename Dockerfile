FROM python:3.9-alpine3.13
LABEL MAINTAINER="ShayestehHS"

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update postgresql-client

COPY ./requirements.txt /requirements.txt

RUN apk add --update --virtual .tmp-deps \
        build-base postgresql-dev musl-dev \
        py-pip jpeg-dev zlib-dev \
        linux-headers python3-dev && \
    /py/bin/pip install -r /requirements.txt

COPY ./scripts /scripts
COPY ./eCommerce /app

WORKDIR /app

RUN apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
#    chmod -R a+rwx ./accounts/migrations/ && \
#    chmod -R a+rwx ./address/migrations/ && \
#    chmod -R a+rwx ./analytics/migrations/ && \
#    chmod -R a+rwx ./carts/migrations/ && \
#    chmod -R a+rwx ./marketing/migrations/ && \
#    chmod -R a+rwx ./orders/migrations/ && \
#    chmod -R a+rwx ./products/migrations/ && \
    chmod -R a+rwx **/migrations/ && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
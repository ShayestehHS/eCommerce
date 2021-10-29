FROM nginxinc/nginx-unprivileged:1-alpine
LABEL MAINTAINER="ShayestehHS"

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000


COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/defult.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

RUN apk add tree

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]
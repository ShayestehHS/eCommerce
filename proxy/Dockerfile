FROM nginx:1.21.3

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params


RUN mkdir -p /vol/static
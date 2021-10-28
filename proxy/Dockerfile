FROM nginx:1.17.9

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params


RUN mkdir -p /vol/static
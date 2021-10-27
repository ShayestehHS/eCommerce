FROM nginx:1.19.0-alpine
LABEL MAINTAINER="ShayestehHS"

COPY ./default.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
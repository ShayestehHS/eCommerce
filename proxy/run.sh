#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

ls

find / -type d -name "static"
#tree -d .
nginx -g 'daemon off;'
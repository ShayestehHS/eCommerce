#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

ls

tree -d var
#tree -d .
nginx -g 'daemon off;'
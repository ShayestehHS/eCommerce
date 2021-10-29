#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

find vol/ -type d -name "message.js"
nginx -g 'daemon off;'
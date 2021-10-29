#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
apt install tree
tree -d .
apt remove tree
nginx -g 'daemon off;'
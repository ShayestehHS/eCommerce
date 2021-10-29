#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
cd var
ls
cd ..
#tree -d .
nginx -g 'daemon off;'
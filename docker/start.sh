#!/bin/bash

echo "Starting uWSGI..."
uwsgi --ini /uwsgi.ini &

echo "Starting Nginx..."
# start nginx in foreground
nginx -g "daemon off;"

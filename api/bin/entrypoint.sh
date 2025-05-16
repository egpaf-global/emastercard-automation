#!/bin/bash

set -x

rm -f /opt/emr-DRC/tmp/pids/server.pid

cd /opt/emr-DRC
bash bin/update_art_metadata.sh development

exec "$@"
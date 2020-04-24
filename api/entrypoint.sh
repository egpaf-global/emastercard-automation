#!/bin/bash

set -x

rm -f /opt/BHT-EMR-API/tmp/pids/server.pid

cd /opt/BHT-EMR-API
rails db:migrate 2> /dev/null

exec "$@"
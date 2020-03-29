#!/bin/bash

rm -f /opt/emastercard/tmp/pids/server.pid

cp /opt/api-config.yml /opt/BHT-EMR-API/config/database.yml || { echo 'Could not locate BHT-EMR-API database configuration'; exit 255; }
cp /opt/migration-config.yml /opt/eMastercard2Nart/config.yaml

exec "$@"
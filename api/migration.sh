#!/bin/bash

if [ ! -f '/opt/eMastercard2Nart/config.yaml']; then
    echo "ERROR: Configuration file not found: api/migration-config.yml"
    exit 255
fi

bash /opt/eMastercard2Nart/migrate.sh

#!/bin/bash

if [ -f '/opt/eMastercard2Nart/config.yaml' ]; then
    bash /opt/eMastercard2Nart/migrate.sh
    correct_missing_dispensations.sh
    exit 0
else
    echo "ERROR: Configuration file not found: api/migration-config.yml"
    exit 255
fi

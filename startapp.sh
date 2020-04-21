#!/bin/bash

echo `pwd`

if [ ! -f "api/api-config.yml" ]; then
    echo 'ERROR: Configuration file `api/api-config.yml` not found or is not a file'
    exit 255
fi

if [ ! -f "api/migration-config.yml" ]; then
    rm -Rf "api/migration-config.yml"   # Could have been autocreated by a previous instance of the application running
    echo '# Override this file by contents from api/migration-config.yml.example' >  api/migration-config.yml
fi

docker-compose up

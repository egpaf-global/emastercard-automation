#!/bin/bash

if [ -t 0 ]; then
    echo "Error: You need redirect or pipe output from a backup file"
    echo "Example: sudo docker-compose exec -T api restore_database.sh < backup.sql"
    exit 255
fi

USERNAME=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['username']"`
PASSWORD=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['password']"`
DATABASE=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['database']"`
HOST=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['host']"`

cd /opt/BHT-EMR-API

echo "Dropping existing database..."
rails db:drop

echo "Creating new database..."
rails db:create

echo "Restoring backup..."
pv -f | mysql --user=$USERNAME --password=$PASSWORD --host=$HOST $DATABASE

echo "Loading metadata..."
cd /opt/BHT-EMR-API
bin/update_art_metadata.sh development


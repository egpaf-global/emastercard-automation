#!/bin/bash

USERNAME=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['username']"`
PASSWORD=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['password']"`
DATABASE=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['database']"`
HOST=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['development']['host']"`

mysqldump --user=$USERNAME --password=$PASSWORD --host=$HOST $DATABASE
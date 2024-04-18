#!/bin/bash

USERNAME=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['${ENV}']['username']"`
PASSWORD=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['${ENV}']['password']"`
DATABASE=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['${ENV}']['database']"`
HOST=`ruby -ryaml -e "puts YAML.safe_load(File.read('/opt/BHT-EMR-API/config/database.yml'), aliases: true)['${ENV}']['host']"`

mysqldump --user=$USERNAME --password=$PASSWORD --host=$HOST $DATABASE
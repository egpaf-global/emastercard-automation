#!/bin/bash

USERNAME=`ruby -ryaml -e "puts YAML::load_file('/opt/BHT-EMR-API/config/database.yml')['development']['username']"`
PASSWORD=`ruby -ryaml -e "puts YAML::load_file('/opt/BHT-EMR-API/config/database.yml')['development']['password']"`
DATABASE=`ruby -ryaml -e "puts YAML::load_file('/opt/BHT-EMR-API/config/database.yml')['development']['database']"`
HOST=`ruby -ryaml -e "puts YAML::load_file('/opt/BHT-EMR-API/config/database.yml')['development']['host']"`

mysqldump --user=$USERNAME --password=$PASSWORD --host=$HOST $DATABASE
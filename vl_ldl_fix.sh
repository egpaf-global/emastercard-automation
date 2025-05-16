#!/bin/bash

echo 'Starting rails process'
date=$(date '+%Y%m%d')
sudo docker-compose exec api fix_vl_ldl_results.sh
echo 'Finished rails process'
echo 'Copying script results'
file=/opt/emr-DRC/vl_to_ldl_migration_$date.csv
sudo docker cp emastercard_api:${file} ./
echo 'Finished'
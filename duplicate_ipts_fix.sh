#!/bin/bash

echo 'Starting rails process'
date=$(date '+%Y%m%d')
sudo docker-compose exec api fix_duplicate_ipts.sh
echo 'Finished rails process'
echo 'Copying script results'
normal_result=/opt/emr-DRC/emc_ipt_duplicates_$date.csv
skipped_result=/opt/emr-DRC/emc_ipt_duplicates_skipped_$(date '+%Y%m%d').csv
sudo docker cp emastercard_api:${normal_result} ./
sudo docker cp emastercard_api:${skipped_result} ./
echo 'Finished'
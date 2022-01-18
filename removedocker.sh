# first of all do a backup of the database
sudo docker-compose exec api backup_database.sh > backup.sql
# second remove docker
sudo apt-get remove docker docker-engine docker.io containerd runc
# Third remove docker engine and the likes
sudo apt-get purge docker-ce docker-ce-cli containerd.io
# Fourth remove docker folders
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
# Fifth stage is to reboot the system so that they can start a fresh
sudo reboot
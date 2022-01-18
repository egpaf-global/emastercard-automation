# first of all do a backup of the database
sudo docker-compose exec api backup_database.sh > backup.sql
# we need to stop the service here
sudo systemctl stop emastercard
# we need to disable the service here
sudo systemctl disable emastercard
# second remove docker
sudo apt-get remove docker docker-engine docker.io containerd runc
# Third remove docker engine and the likes
sudo apt-get purge docker-ce docker-ce-cli containerd.io
# Fourth remove docker folders
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
# Fifth stage is to reboot the system so that they can start a fresh
sudo reboot
# eMastercard Upgrade Automation

A set of tools to ease upgrade of emastercard 3.* to the new emastercard.

## Build and install

```bash
./setup.py
```
- This command pulls all necessary dependencies and builds a docker container for the application.
- The command also sets up a stub in `/usr/local/bin` for starting the application thus the
  application can be started from anywhere by running the `emastercard` command.

## Start the application

The are two ways to start the application, the following command may be run at the root of
the `emastercard-upgrade-automation` folder.

```bash
sudo docker-compose up
```
- NOTE: The rest of the commands below require that this command be run first.
  All `docker-compose exec` require the application to be running. 

## Initializing the database

```bash
sudo docker-compose exec api initialize_database.sh
```

- WARNING: This command resets the database to a clean (and empty) state.

## Running the migration

Ensure that both the old and new emastercards are running then run the following:

```bash
sudo docker-compose exec api migration.sh
```

- At the end of the migration, a number of reports are dumped into the `tmp` folder
  The reports are: migration-errors.yml, outcomes-report.csv.

## Backing up the database

```bash
sudo docker-compose exec api backup_database.sh > backup.sql
```

## For developers

To update the frontend's static files do the following:

```bash
$ ./setup.py --rebuild-frontend
$ git add web/static/*
$ git commit -m 'Some commit message'
$ git push
```


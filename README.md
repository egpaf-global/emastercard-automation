# eMastercard Upgrade Automation

A set of tools to ease upgrade of emastercard 3.* to the new emastercard.

## Build and install

```bash
./setup.py
```

## Start the application

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

```bash
sudo docker-compose exec api migration.sh
```

- At the end of the migration, a number of reports are dumped into the `tmp` folder
  The reports are: migration-errors.yml, outcomes-report.csv.

## Backing up the database

```bash
sudo docker-compose exec api backup_database.sh > backup.sql
```

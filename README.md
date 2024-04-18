# eMastercard Upgrade Automation

A set of tools to ease upgrade of emastercard 3.* to the new emastercard.

## Configure the application

1. Change the root database password in `docker-compose.yml` and `docker-compose-build.yml`
   NOTE: The database password defaults to `password` which is highly insecure.

2. Copy the example configuration files for the api and the migration scripts.

    ```bash
      cp api/api-config.yml.example api/api-config.yml
      cp api/migration-config.yml.example api/migration-config.yml
    ```
    <h1 style="color:red;">Please use new configurations going forward.</h1>

3. Edit the two configuration files created in the previous step setting the database
   passwords for the API and the old eMastercard application.

   NOTE: In the `migration-config.yml`, the `api` is under section `emr` and the `old
   emastercard` is under the `emastercard` section. The `site_prefix` in the
   `migration-config.yml` has to be set for the migration to run at all. That prefix
   is used to create patient identifiers in the migrated database. For more information
   on what the various fields in the migration configuration file mean, see the configuration
   section of the following: [eMastercard2Nart](https://github.com/HISMalawi/eMastercard2Nart/blob/master/README.md).

## Build and installation

NOTE: The installation requires an internet connection through out the installation process.

1. The following comand builds and installs the application:

    ```bash
      ./setup.py
    ```
   A service file that automatically starts the application is created thus the status of
   application can be queried like so:

    ```bash
      sudo systemctl status emastercard
    ```

2. The setup above simply creates the application with an empty database. To initialize
   the database execute the following:

    ```bash
      sudo docker-compose exec api initialize_database.sh
    ```

  - WARNING: This command truncates all tables and loads the base metadata to the database.

3. Migrating data from the old emastercard to the new one, requires that both the old emastercard
   and new emastercard be running. To start the migration do the following:

    ```bash
      sudo docker-compose exec api migration.sh
    ```

   At the end of the migration, a number of reports are dumped into the `tmp` folder.
   The reports are: migration-errors.yml, outcomes-report.csv.

## Offline installations

It's possible to use a pre-existing installation to create installers that can be used
for offline installations. For information on how this can be done, please refer to the
[Offline installation](docs/offline-installation.md) document.

## Updating the application

  ```bash
    git pull -f origin master && ./setup.py
  ```

## Database mantainance

- To `backup` the database run the following command in the `emastercard-upgrade-automation`
  directory:

    ```bash
      sudo docker-compose exec api backup_database.sh > backup.sql
    ```

- To `restore` the database run the following command in the `emastercard-upgrade-automation`
  directory. 

    ```bash
      sudo docker-compose exec -T api restore_database.sh < backup.sql
    ```

- To `change the database password` do the following:

    ```bash
      sudo docker-compose exec api change_database_password.sh
    ```

## Troubleshooting the application

Below are basic instructions for troubleshooting issues with the application.
For more detailed information on troubleshooting please visit the
[troubleshooting](docs/troubleshooting.md) page.

- Manually start the application by running the following and checking for errors in the
  output:

  ```bash
    sudo docker-compose up
  ```

  In some cases you may notice that the application is still pulling the nginx and mysql
  containers. These are usually pulled when the application first starts up thus why
  an internet connection is needed through out the installation process.

- Restart the application if the configuration file(s) where changed as follows:

  ```bash
    sudo systemctl restart emastercard
  ```

- Rebuild the containers as follows:

  ```bash
    sudo docker-compose -f docker-compose-build.yml build

    sudo systemctl restart emastercard
  ```

- Look at past logs to see what was going wrong:

  ```bash
    sudo journalctl -u emastercard
  ```

  NOTE: If the log file gets too big and you are having problems reading the log, you can trim
  it down like so (this leaves 7 days worth of log files):

  ```bash
    sudo journalctl --vacuum-time=7d
  ```

- In some cases you may need to run the latest updates for the application, run the following
  command:

  ```bash
    git pull -f && ./setup.py --no-follow-tags
  ```
- In some cases the setup my crush and continue to show you errors. In such scenarios you can use
  this script to remove docker completely and do a fresh install:

  ```bash
    ./removedocker.sh
  ```

## For developers

To update the frontend's static files do the following:

  ```bash
    $ ./setup.py --rebuild-frontend
    $ git add web/static/*
    $ git commit -m 'Some commit message'
    $ git push
  ```

## Automation Scripts

#### Update viral load results bearing =1 to =LDL
- The script migrates all `HIV viral load` results `=1` to `=LDL`. to run the script, please type the following command

```bash
sh vl_ldl_fix.sh
```

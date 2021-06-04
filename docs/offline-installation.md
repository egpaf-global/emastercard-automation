# eMastecard offline installation

This document describes how one can build an image of the eMastercard
application for offline installation.

1. Preparing the image on a machine with an internet connection.
    - Requirements:
        - An internet connection
        - A working eMastercard installation.
    - Navigate to the [emastercard-upgrade-automation](https://github.com/HISMalawi/emastercard-upgrade-automation) folder then execute the following commands:

        ```bash
        $ git pull
        $ ./setup.py
        $ ./setup.py --package-for-offline
        ```
    - The steps above will create a tarball named `emastercard-upgrade-automation.tgz` in
      the tmp folder. This tarball can be transferred to and installed on machines
      without an internet connection. 

2. Installing the image
    - Requirements:
        - docker
        - docker-compose
        - NOTE: The old eMastercard installations used these same application, you
          don't need to reinstall them.
    - Copy the installer created in the step above to the target machine.
    - Extract the tarball as the follows:

        ```bash
        $ tar -xzvf emastercard-upgrade-automation.tgz
        ```

    - Go into the created `emastercard-upgrade-automation` folder and configure the
      application as you normally do; setting the database password and site_prefix
      in `api/migration-config.yml`.

    - Install the application as follows:

        ```
        $ ./setup.py --offline
        ```
        
    - If this is a completely new installation not an update then you should do
      the following:

      ```
      % sudo docker-compose exec api initialize_database.sh
      ```

    - Once the installation completes go to http://localhost:8000 in your browser to
      verify that application is up and running. NOTE: For new installations you should
      proceed with the steps 
    

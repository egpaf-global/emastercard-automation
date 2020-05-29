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
        $ ./setup.py --cache-images
        $ cd ..
        $ tar -cz emastercard-upgrade-automation ../emastercard-upgrade-automation.tgz
        ```
    - The steps above will create tarball, `emastercard-upgrade-automation.tgz,
      which can be extracted and installed on a machine without an internet connection.

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
        $ sudo docker-compose exec api initialize_database.sh
        ```

    - Once the installation completes go to http://localhost:8000 in your browser to
      verify that application is up and running.
    

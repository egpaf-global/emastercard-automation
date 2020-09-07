# Troubleshooting

This section documents issues that may be faced during installation
of the application or as the application is operating. Possible
solutions for the problems are provided. Please note the primary
focus here is the backend pieces of the application and not user
interface related problems, for those you may want to look at the
[e-Mastercard](https://github.com/EGPAFMalawiHIS/emastercard)
repository.

## Accessing application's logs

When facing an issue, the first place you may want to go to is the
application's logs. The logs will provide detailed information on
which of the application's components is failing and why. There are
a number of ways to access the logs, below is a list of them:

1. Attaching to the application's STDOUT (easiest)

   Running the following command in the application's root directory
   attaches to the STDOUT/STDERR streams of a running instance of the
   application (it attempts to start the application if not already
   running). 

    ```bash
      sudo docker compose up
    ```

   Note that the command above only gives a partial view of the logs.
   Specifically you get the current application's output, not all
   historical logs.

2. Checking application's status in systemd

   This is useful if the application is completely inaccessible from
   a web browser. The level of detail you get from this will mostly
   be limited to "is the application up or down" and possibly a reason
   as to why it has failed to start in cases where there is a problem
   with the application's unit file.

    ```bash
      sudo systemctl status emastercard
    ```
3. Accessing the application's full log

   This method gives access to almost every single line the application
   has ever output (unless the logs were cleared at some point).
   
    ```bash
      sudo journalctl -u emastercard
    ```

   Take note that since the logs can grow so big, navigating the output can
   be a bit slow. Press &lt;SHIFT-g&gt; to jump to the end of the logs.
   From there you can scroll upwards. This entire process may be somewhat
   sluggish depending on the size of the logs. If you need to clear out the
   logs, you may want to consider `sudo journalctl --vacuum-time=?`,
   `sudo journalctl --vacuum-size=?`, and related commands. Lookup
   `man journalctl` for more details.

## Quick fixes (for most stuff)

Some of the application's problems can be fixed by simply restarting the
application (or power-cycling the computer - yes it works, sometimes).
For example, problems to do with migrations and metadata can easily be
fixed by restarting the application and waiting for some seconds
(at most 60 seconds). The application attempts to run migrations and
load metadata at startup. However for build related problems and
`you need to force a rebuild of the application` then do the following:

  ```bash

    sudo systemctl stop emastercard

    sudo docker-compose -f docker-compose-build.yml build

    sudo docker-compose up # Manually start application to pull additional containers

    # When all is done and is working correctly, stop the application by
    # hitting <Ctrl-C> then starting the systemd service.

    sudo systemctl start emastercard

  ```

## Specific (nasty) problems that may be encountered

Below are some of the problems that have been met in the past during
deployments and updating of the application.

### Couldn't connect to Docker daemon at http-docker://localunixsocket

This is almost always due to docker not running. Start it as follows:

  ```bash

    sudo systemctl start docker

    sudo systemctl status docker # To check whether it's up

  ```

### Cannot start service ... Read only file system

This is a result of docker failing to create mount points for various
files the application uses. It can be a general permission issue where
the solution might simply be to correct the permissions of the paths
docker is complaining about. In most cases that have been observed
however the main issue is the docker itself. Docker that is installed
through [snap](https://snapcraft.io/docs/installing-snap-on-ubuntu)
does not allow docker applications to access paths outside user's
home directories (ie `/home/username`). For security reasons some of
the applications mount points are placed in `/opt` thus when trying
to run the application through snap's docker, the application will
fail with the `read only file system` error. To deal with the problem
there are two possible solutions, the first being removing the
abomination that is docker installed through snap and installing it
via apt. Try the following to do it:

  ```bash

  sudo snap remove docker

  sudo apt install docker-io docker-compose

  ```

The second method involves changing the mount points in the docker
compose files. To do this, open `docker-compose.yml` and
`docker-compose-build.yml`. Then replace `/opt/emastercard/db` with
a path in a user's home directory, for example
`/home/user/.emastercard/db`. NOTE: You may have to do this everytime
you `git pull` and/or `git checkout`. To minimise headaches during
updates thus the first method is recommended.

### ... tmpdir: could not find a temporary directory ... bundle install returned a non-zero ...

This error occurs when setup.py is called. Building of the docker
containers fails due to having invalid permissions on
`/var/lib/docker/tmp` (for docker installed by snap, you need to
find out where that directory is placed). The main cause for this
is user error (ie someone run `sudo chmod -R 777 /var` or something
similar). You can fix this by either changing the permissions for
the file back to 700 or purging docker and reinstalling as follows:

  ```bash

    # 1. Fixing permissions

    sudo chmod 700 /var/lib/docker/tmp

    ./setup.py

    # Or 2. Re-installing docker

    sudo apt purge docker-io

    sudo apt install docker-io docker-compose

    ./setup.py
  ```
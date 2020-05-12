#!/usr/bin/env python

import json
import os
import os.path
import re
import sys

REBUILD_FRONTEND = False
FOLLOW_TAGS = True

for arg in sys.argv[1:]:
    if arg == '--rebuild-frontend':
        REBUILD_FRONTEND = True
        break
    elif arg == '--no-follow-tags':
        FOLLOW_TAGS = False

def run(command, die_on_fail=True):
    print('Running: {command}'.format(command=command))
    if os.system(command) == 0:
        return True

    sys.stderr.write('error: Operation failed: {command}\n'.format(command=command))
    if die_on_fail:
        exit(255)    

    return False

def update_repo(repository, branch='master', follow_tags=True):
    '''Clones or updates a repository.'''
    print('Cloning/updating repository: {repository}'.format(repository=repository))
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    os.chdir('tmp')
    dir_name = re.sub(r'.git$', '', os.path.basename(repository))

    if not os.path.exists(dir_name):
        run('git clone {repository}'.format(repository=repository))

    os.chdir(dir_name)
    run('git checkout -f {}'.format(branch))
    run('git pull -f origin {}'.format(branch))

    if follow_tags:
        run('git fetch --tags')
        run('git checkout -f `git describe --tags`')

    os.chdir('../..')

    print('------------------')

def build_emastercard_frontend(follow_tags):
    print('Building eMastercard frontend; this may take a while...')
    update_emastercard_frontent_config(follow_tags=follow_tags)
    os.chdir('tmp/e-Mastercard')
    run('npm install')
    run('npm run build')
    os.chdir('../..')
    run('rm -Rv web/static/*')
    run('cp -Rv tmp/e-Mastercard/dist/* web/static')
    print('-----------------')

def update_emastercard_frontent_config(deploy_path='tmp/e-Mastercard/public/config.json', follow_tags=True):
    def get_frontend_version():
        if not os.path.exists('tmp/e-Mastercard'):
            return '4.0-dev'

        def read_gitcmd_output(command):
            return os.popen('git -C tmp/e-Mastercard {}'.format(command))\
                     .readline()\
                     .strip()

        if follow_tags:
            return read_gitcmd_output('describe')
        else:
            commit = read_gitcmd_output('log').replace('commit ', '')[:7]
            return '4.0-{}'.format(commit)
                          
    def read_frontend_config():
        with open('web/config.json') as fin:
            return json.loads(fin.read())

    def save_frontend_config(config):
        with open(deploy_path, 'w') as fout:
            fout.write(json.dumps(config))

    print('Updating frontend configuration...')
    config = read_frontend_config()
    config['version'] = get_frontend_version()
    save_frontend_config(config)

def build_docker_container():
    print('Building docker container...')
    run('sudo docker-compose build')
    print('-----------------')

def setup_dependencies():
    print('Setting up dependencies...')
    # Some setups have messed repository sources that break the following step.
    # Ignore the errors and just go ahead with the installation of docker.
    run('sudo apt-get update', die_on_fail=False)
    if REBUILD_FRONTEND:
        run('sudo apt-get install -y docker.io docker-compose git nodejs npm')
    else:
        run('sudo apt-get install -y docker.io docker-compose git')
    print('-----------------')

SYSTEMD_SERVICE_TEMPLATE = '''
[Unit]
Description = Emastercard web service
After       = network.target

[Service]
WorkingDirectory={install_dir}
ExecStart=/bin/bash {install_dir}/startapp.sh 
ExecStop=/bin/bash {install_dir}/stopapp.sh
ExecReload=/bin/bash {install_dir}/restartapp.sh

# In case if it gets stopped, restart it immediately
Restart     = always

Type        = simple


[Install]
# multi-user.target corresponds to run level 3
# roughtly meaning wanted by system start
WantedBy    = multi-user.target
'''

def setup_autostart():
    print('Setting up emastercard autostart: tmp/emastercard.service')
    with open('tmp/emastercard.service', 'w') as service_file:
        service_file.write(SYSTEMD_SERVICE_TEMPLATE.format(install_dir=os.getcwd()))

    run('sudo systemctl stop emastercard.service', die_on_fail=False)
    run('sudo cp tmp/emastercard.service /etc/systemd/system')
    run('sudo systemctl enable emastercard.service')
    print('eMastercard has been set to automatically start up at boot time.')

    if os.path.isfile('api/api-config.yml'):
        run('sudo systemctl start emastercard.service')
        print("Application started... Go to http://localhost:8000 to verify if application is up")
    else:
        print("Warning: Application not started due to missing configuration files: api/api-config.yml")
        print("=> Please create the configuration file by copying api/api-config.yml.example and then editing the copied file accordingly")
        print("=> Run `sudo systemctl start emastercard.service` to start the application")



if os.path.exists('tmp/db'):
    # Had database files in directory users may consider clearing.
    # Have to move to somewhere somewhat secure.
    print('Moving database directory to /opt/emastercard...')
    run('sudo systemctl stop emastercard', die_on_fail=False)

    if not os.path.exists('/opt/emastercard'):
        run('sudo mkdir /opt/emastercard')

    run('sudo mv tmp/db /opt/emastercard')

setup_dependencies()
update_repo('https://github.com/HISMalawi/BHT-EMR-API.git', branch='development', follow_tags=FOLLOW_TAGS)
update_repo('https://github.com/HISMalawi/eMastercard2Nart.git', follow_tags=False)
if REBUILD_FRONTEND:
    update_repo('https://github.com/EGPAFMalawiHIS/e-Mastercard.git', branch='development', follow_tags=FOLLOW_TAGS)
    build_emastercard_frontend(FOLLOW_TAGS)
build_docker_container()
setup_autostart()

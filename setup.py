#!/usr/bin/env python

import os
import os.path
import re
import sys

for arg in sys.argv[1:]:
    if arg == '--rebuild-frontend':
        REBUILD_FRONTEND = True
        break
else:
    REBUILD_FRONTEND = False

def run(command, die_on_fail=True):
    print('Running: {command}'.format(command=command))
    if os.system(command) == 0:
        return True

    sys.stderr.write('error: Operation failed: {command}\n'.format(command=command))
    if die_on_fail:
        exit(255)    

    return False

def update_repo(repository, branch='master'):
    '''Clones or updates a repository.'''
    print('Cloning/updating repository: {repository}'.format(repository=repository))
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    os.chdir('tmp')
    dir_name = re.sub(r'.git$', '', os.path.basename(repository))

    if os.path.exists(dir_name):
        os.chdir(dir_name)
        run('git checkout {branch}'.format(branch=branch))
        run('git pull origin {branch}'.format(branch=branch))
        os.chdir('..')
    else:
        run('git clone {repository}'.format(repository=repository))
        os.chdir(dir_name)
        run('git checkout {branch}'.format(branch=branch))
        os.chdir('..')

    os.chdir('..')
    print('------------------')

def build_emastercard_frontend():
    print('Building eMastercard fronted; this may take a while...')
    emastercard_build_dir = os.path.join('e-Mastercard', 'dist')
    emastercard_install_dir = os.path.join('BHT-EMR-API', 'public')

    run('cp web/config.json tmp/e-Mastercard/public/config.json')
    os.chdir('tmp/e-Mastercard')
    run('npm install')
    run('npm run build')
    os.chdir('../..')
    run('cp -Rv tmp/e-Mastercard/dist/* web/static')
    print('-----------------')

def build_docker_container():
    print('Building docker container...')
    run('sudo docker-compose build')
    print('-----------------')

def setup_dependencies():
    print('Setting up dependencies...')
    run('sudo apt-get update')
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
ExecStart=bash {install_dir}/startapp.sh 
ExecStop=/bin/kill -INT $MAINPID
ExecReload=/bin/kill -TERM $MAINPID

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
    print('-----------------------')


# setup_dependencies()
# update_repo('https://github.com/HISMalawi/BHT-EMR-API.git', branch='development')
# update_repo('https://github.com/HISMalawi/eMastercard2Nart.git')
# if REBUILD_FRONTEND:
#     update_repo('https://github.com/EGPAFMalawiHIS/e-Mastercard.git', branch='development')
#     build_emastercard_frontend()
build_docker_container()
setup_autostart()

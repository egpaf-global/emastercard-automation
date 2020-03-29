#!/usr/bin/env python

import os
import os.path
import re
import sys

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
    print('-----------------')

def build_docker_container():
    print('Building docker container...')
    run('sudo docker-compose build')
    print('-----------------')

def setup_dependencies():
    print('Setting up dependencies...')
    run('sudo apt-get update')
    run('sudo apt-get install -y docker.io docker-compose git nodejs npm')
    print('-----------------')

setup_dependencies()
update_repo('https://github.com/HISMalawi/BHT-EMR-API.git', branch='development')
update_repo('https://github.com/HISMalawi/eMastercard2Nart')
update_repo('https://github.com/EGPAFMalawiHIS/e-Mastercard', branch='development')
build_emastercard_frontend()
build_docker_container()

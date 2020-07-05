#!/usr/bin/env python

import argparse
import json
import os
import os.path
import re
import sys

FOLLOW_TAGS = True
OFFLINE = False
REBUILD_FRONTEND = False
UPDATE = False

def run(command, die_on_fail=True):
    print('Running: {command}'.format(command=command))
    if os.system(command) == 0:
        return True

    sys.stderr.write('error: Operation failed: {command}\n'.format(command=command))
    if die_on_fail:
        exit(255)    

    return False

def update_repo(repository, branch='master', tag=None):
    '''Clones or updates a repository.'''
    def get_tag():
        run('git fetch --tags -f')
        
        if tag is None:
            return '`git describe --tags`'
            
        return tag

    print('Cloning/updating repository: {repository}'.format(repository=repository))
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    os.chdir('tmp')
    dir_name = re.sub(r'.git$', '', os.path.basename(repository))

    if not os.path.exists(dir_name):
        run('git clone {repository}'.format(repository=repository))

    os.chdir(dir_name)
    run('git checkout -f {}'.format(branch))
    run('git pull --rebase=false -f origin {}'.format(branch))

    if FOLLOW_TAGS:
        run('git checkout -f {}'.format(get_tag()))

    os.chdir('../..')
    return read_tag(os.path.join('tmp', dir_name))

def read_gitcmd_output(repo, command):
    return os.popen('git -C {} {}'.format(repo, command))\
             .readline()\
             .strip()

def read_tag(repo):
    if FOLLOW_TAGS:
        return read_gitcmd_output('{}'.format(repo), 'describe --tags')
    else:
        return None

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
    def get_latest_commit_id():
        return read_gitcmd_output('.', 'log').split()[1]
                         
    def read_frontend_config():
        with open('web/config.json') as fin:
            return json.loads(fin.read())

    def save_frontend_config(config):
        with open(deploy_path, 'w') as fout:
            fout.write(json.dumps(config))

    print('Updating frontend configuration...')
    config = read_frontend_config()
    version = read_tag(os.getcwd()) or get_latest_commit_id()[:7]
    config['version'] = 'docker-{}'.format(version)
    save_frontend_config(config)

IMAGE_NAMES = ['emastercard_api', 'nginx', 'mysql']

def dump_images():
    print('Dumping docker images...')
    if not os.path.exists('tmp/images'):
        os.makedirs('tmp/images')

    for name in IMAGE_NAMES:
        print('Dumping image {}'.format(name))
        run('sudo docker save {name} -o tmp/images/{name}'.format(name=name))

def load_images():
    print("Looking for local docker images...")
    if not os.path.exists('tmp/images'): return None

    for file in os.listdir('tmp/images'):
        print('Loading image tmp/images/{}'.format(file))
        run('sudo docker load -i tmp/images/{}'.format(file))
      
def build_docker_container():
    print('Building docker container...')
    run('sudo docker-compose -f docker-compose-build.yml build --pull')
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

def load_tags():
    import json

    if UPDATE or not os.path.exists('TAGS'):
        return {}

    with open('TAGS') as fin:
        return json.loads(fin.read())

def save_tags(tags):
    with open('TAGS', 'w') as fout:
        fout.write(json.dumps(tags))

def offline_build():
    load_images()
    build_docker_container(offline=True)
   
def build():
    if os.path.exists('tmp/db'):
        # Had database files in directory users may consider clearing.
        # Have to move to somewhere somewhat secure.
        print('Moving database directory to /opt/emastercard...')
        run('sudo systemctl stop emastercard', die_on_fail=False)

        if not os.path.exists('/opt/emastercard'):
            run('sudo mkdir /opt/emastercard')

        run('sudo mv tmp/db /opt/emastercard')

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    if not OFFLINE:
        tags = load_tags()

        setup_dependencies()
        tags['BHT-EMR-API'] = update_repo('https://github.com/HISMalawi/BHT-EMR-API.git', branch='development', tag=tags.get('BHT-EMR-API'))
        tags['eMastercard2Nart'] = update_repo('https://github.com/HISMalawi/eMastercard2Nart.git', branch='master', tag=tags.get('eMastercard2Nart'))
        if REBUILD_FRONTEND:
            tags['e-Mastercard'] = update_repo('https://github.com/EGPAFMalawiHIS/e-Mastercard.git', branch='development', tag=tags.get('e-Mastercard'))
            build_emastercard_frontend(FOLLOW_TAGS)

        if UPDATE:
            save_tags(tags)
            
        build_docker_container()
    else:
        load_images()

    setup_autostart()

def read_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--no-follow-tags', action='store_true', help='Build application on the latest commit/update instead of latest tag')
    parser.add_argument('--dump-images', action='store_true', help='Dump all images into local cache to enable offline installs')
    parser.add_argument('--offline', action='store_true', help='Attempt to build application using cached resources only')
    parser.add_argument('--rebuild-frontend', action='store_true', help='Forces a rebuilding of the frontend')
    parser.add_argument('--update', action='store_true', help='Updates all applications to latest updates/tags')
    
    return parser.parse_args()

def main():
    global FOLLOW_TAGS, OFFLINE, REBUILD_FRONTEND, UPDATE

    args = read_arguments()

    if args.no_follow_tags: FOLLOW_TAGS = False
    if args.offline: OFFLINE = True
    if args.rebuild_frontend: REBUILD_FRONTEND = True
    if args.update: UPDATE = True

    if args.dump_images:
        dump_images()
    else:
        build()

if __name__ == '__main__':
    main()


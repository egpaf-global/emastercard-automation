#!/usr/bin/env python3

import argparse
import json
import os
import os.path
import re
import sys

FOLLOW_TAGS = True
OFFLINE = False
REBUILD_FRONTEND = False
SYSTEMD_CONFIG = True   # Configure systemd to autostart the emastercard application
UPDATE = False
IMAGE_NAMES = ['emastercard_api', 'nginx', 'mysql']

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
        run('git remote prune origin')
        run('git fetch --tags -f')
        
        if UPDATE:
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
    os.chdir('tmp/emc-new-arch')
    run('npm install --global @ionic/cli@latest')
    run('npm install --global @vue/cli@latest')
    run('npm install --legacy-peer-deps')
    run('ionic build')
    os.chdir('../..')
    run('pwd')
    run('rm -rfv web/static/*')
    run('cp -rv tmp/emc-new-arch/dist/* web/static/')
    print('-----------------')

def make_offline_package():
    print('Dumping docker images...')
    if not os.path.exists('tmp/images'):
        os.makedirs('tmp/images')

    for name in IMAGE_NAMES:
        print('Dumping image {}'.format(name))
        run('sudo docker save {name} -o tmp/images/{name}'.format(name=name))
        
    print('Packaging to emastercard.tgz...')
    run("sudo bash -c 'tar -czvf tmp/emastercard-upgrade-automation.tgz $(git ls-files) tmp/images/ .git/'")
    run('sudo chmod a+rw tmp/emastercard-upgrade-automation.tgz')
    print('Package successfully created at tmp/emastercard-upgrade-automation.tgz')

def load_images():
    print("Looking for local docker images...")
    if not os.path.exists('tmp/images'):
        print('Error: Missing docker images in tmp/images')
        exit(255)

    for file in os.listdir('tmp/images'):
        print('Loading image tmp/images/{}'.format(file))
        run('sudo docker load -i tmp/images/{}'.format(file))
      
def build_docker_container():
    print('Building docker container...')
    run('sudo docker-compose -f docker-compose-build.yml build --pull')
    print('-----------------')
    
def check_docker_compose_version(target_version):
    version_string = os.popen('docker-compose --version').readline().strip()
    if not version_string:
        return None

    return re.match(r'docker-compose version\s+{},.*$'.format(target_version), version_string) != None

def install_docker_compose():
    print('Checking docker-compose version...')
    version = '1.29.0'
    if check_docker_compose_version(version):
        print('Found docker-compose version {}'.format(version))
        return None
    print('Installing docker-compose version {}'.format(version))
    run('sudo apt-get install -y curl')
    isa = os.popen('uname -m').readline().strip()
    run('sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-Linux-{}" -o /usr/local/bin/docker-compose'.format(isa))
    run('sudo chmod +x /usr/local/bin/docker-compose')

def setup_dependencies():
    print('Setting up dependencies...')
    # Some setups have messed repository sources that break the following step.
    # Ignore the errors and just go ahead with the installation of docker.
    run('sudo apt-get update', die_on_fail=False)
    run('sudo apt-get install -y docker.io git')
    install_docker_compose()
    if REBUILD_FRONTEND and os.system('npm --version') != 0:
        run('sudo apt-get install -y nodejs npm', die_on_fail=False) # Not sma
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

def load_version_info():
    import json

    if not os.path.exists('.version'):
        return {'tags': {}}

    with open('.version') as fin:
        version_info = json.loads(fin.read())
        
        return version_info

def save_version_info(version_info):
    with open('.version', 'w') as fout:
        fout.write(json.dumps(version_info, indent=2))

def offline_build():
    load_images()
    build_docker_container()
    
def update_version(current_version, tags):
    if current_version is None:
        return '0.0.1-0'

    version_parts = current_version.split('-', 1)
    frontend_version = '-'.join(version_parts[:-1])
    
    if not version_parts[-1].isdigit():
        _codename, revision = version_parts[-1].split('-')
    else:
        revision = version_parts[-1]
        
    revision = int(revision)
    
    if tags['e-Mastercard'] == frontend_version:
        revision += 1
    else:
        frontend_version = tags['e-Mastercard']
        revision = 0
        
    return '{}-{}'.format(frontend_version, revision)


   
def build():
    if os.path.exists('tmp/db'):
        
        print('Moving database directory to /opt/emastercard...')
        run('sudo systemctl stop emastercard', die_on_fail=False)

        if not os.path.exists('/opt/emastercard'):
            run('sudo mkdir /opt/emastercard')

        run('sudo mv tmp/db /opt/emastercard')

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    version_info = load_version_info()
    version = version_info.get('version')
    tags = version_info.get('tags', {})

    if not OFFLINE:
        setup_dependencies()
        tags['BHT-EMR-API'] = update_repo('https://github.com/egpaf-global/emr-DRC.git', branch='main', tag=tags.get('BHT-EMR-API'))
        os.chdir('tmp/BHT-EMR-API')
        run('git describe > HEAD')
        os.chdir('../..')
        
        tags['eMastercard2Nart'] = update_repo('https://github.com/HISMalawi/eMastercard2Nart.git', branch='master', tag=tags.get('eMastercard2Nart'))
        if REBUILD_FRONTEND:
            tags['e-Mastercard'] = update_repo('https://github.com/egpaf-global/e-mastercard-core.git', branch='main', tag=tags.get('e-Mastercard'))
            build_emastercard_frontend(FOLLOW_TAGS)

        if UPDATE:
            version = update_version(version, tags)
            save_version_info({'version': version, 'tags': tags})
            
        build_docker_container()
    else:
        load_images()


    if SYSTEMD_CONFIG:
        setup_autostart()

def read_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--configure-host-address', action='store_true', help='Automatically detects ip address and updates host in e-Mastecard configuration')
    parser.add_argument('--package-for-offline', action='store_true', help='Creates a package for offline installations')
    parser.add_argument('--no-follow-tags', action='store_true', help='Build application on the latest commit/update instead of latest tag')
    parser.add_argument('--no-systemd-config', action='store_true', help='Disables creation/update of unit file for systemd')
    parser.add_argument('--offline', action='store_true', help='Attempt to build application using cached resources only')
    parser.add_argument('--rebuild-frontend', action='store_true', help='Forces a rebuilding of the frontend')
    parser.add_argument('--update', action='store_true', help='Updates all applications to latest updates/tags')
    
    return parser.parse_args()

def main():
    global FOLLOW_TAGS, OFFLINE, REBUILD_FRONTEND, SYSTEMD_CONFIG, UPDATE

    args = read_arguments()

    if args.no_follow_tags: FOLLOW_TAGS = False
    if args.offline: OFFLINE = True
    if args.rebuild_frontend: REBUILD_FRONTEND = True
    if args.update: UPDATE = True
    if args.no_systemd_config: SYSTEMD_CONFIG = False

        
    if args.package_for_offline:
        make_offline_package()
        exit()

    build()

if __name__ == '__main__':
    main()


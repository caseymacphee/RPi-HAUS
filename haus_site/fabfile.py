# Setup and install RPi-Haus, from the haus_site directory
# 1. Provision instance:
#       fab provision_instance
# 2. Update image, install packages
#       fab install_django_haus
# 3. Setup Postgres database
#       fab setup_haus_database
# 4. Start the server
#       fab start_server
# For utility
#       fab create_superuser
#       fab ssh
#       fab refresh_django_app
# The last restarts gunicorn (pulling in any changes you made since last
# starting it)
# Note that for actual deployment the settings file should be edited
# to turn off debug and set ALLOWED_HOSTS = ['127.0.0.1']

from fabric.api import task, cd, run, env, prompt, execute, sudo, open_shell
from fabric.api import settings, put
import fabric.contrib
import time
import os
# import io
import boto
import boto.ec2
from haus_site import credentials

env.hosts = ['localhost', ]
env["user"] = "ubuntu"
env["key_filename"] = "~/.ssh/fabric.pem"  # Update to user
env.aws_region = 'us-west-2'


@task
def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


@task
def provision_instance(wait_for_running=False, timeout=60,
                       interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't2.micro'
    key_name = 'fabric'
    security_group = 'ssh-access'
    image_id = "ami-3d50120d"
    # subnet_id = create_network()  # Probably don't want to do this each time

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ],
    )
    new_instances = [i for i in reservations.instances
                     if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()

    elastic_ip = conn.allocate_address(domain="vpc")
    conn.associate_address(instance_id=reservations.instances[0].id,
                           allocation_id=elastic_ip.allocation_id)


@task
def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        env.user + '@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


def _install_haus_requirements():
    sudo('apt-get update')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install python-pip')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install postgresql-9.3')
    sudo('apt-get -y install postgresql-server-dev-9.3')
    sudo('apt-get -y install git')
    sudo('apt-get -y install nginx')

    if not fabric.contrib.files.exists('~/RPi-HAUS/'):
        with settings(warn_only=True):
            sudo('git clone https://github.com/caseymacphee/RPi-HAUS.git')
    sudo('ln -s /home/ubuntu/RPi-HAUS/nginx.conf ' +
         '/etc/nginx/sites-enabled/amazonaws.com')
    with cd('RPi-HAUS'):
        sudo('pip install -r requirements.txt')
    sudo('shutdown -r now')


def _setup_database():
    credentials.set_credentials()
    password = os.environ['DATABASE_PASSWORD']
    create_user_command = """"
  create user haus with password '%s';
  grant all on database haus to haus;"
""" % password
    with settings(warn_only=True):
        sudo('createdb haus', user='postgres')
    sudo('psql -U postgres haus -c %s' % create_user_command, user='postgres')


def _get_secrets():
    if not fabric.contrib.files.exists('~/RPi-HAUS/haus_site/' +
                                       'haus_site/credentials.py'):
        secrets_file_name = \
            raw_input("Enter the name & path of the credentials.py file: ")
        secrets_file_name = put(secrets_file_name, '.')[0]
        sudo('mv %s ~/RPi-HAUS/haus_site/haus_site/credentials.py' %
             secrets_file_name)


def _start_server():
    _get_secrets()
    sudo('/etc/init.d/nginx restart')
    with cd('RPi-HAUS'):
        sudo('pip install -r requirements.txt')
    with cd('RPi-HAUS/haus_site'):
        sudo('python manage.py migrate')
        with settings(prompts=
                      {"Type 'yes' to continue, or 'no' to cancel: ": 'yes'}):
            sudo('python manage.py collectstatic')
        sudo('gunicorn -b 127.0.0.1:8888' + ' haus_site.wsgi:application')


def _refresh_django_app():
    _get_secrets()
    with cd('~/RPi-HAUS/haus_site'):
        sudo('python manage.py migrate')
    run('ps -a|grep gunicorn')
    masterpid = raw_input("Enter gunicorn master PID number: ")
    sudo('kill -s HUP %s' % masterpid)
    print "Gunicorn restarted"


def _create_superuser():
    _get_secrets()
    with cd('RPi-HAUS/haus_site'):
        sudo('python manage.py migrate')
        sudo('python manage.py createsuperuser')


def _install_nginx():
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


def _set_cronjob():
    sudo('crontab /home/ubuntu/RPi-HAUS/crondump.txt')


@task
def refresh_django_app():
    run_command_on_selected_server(_refresh_django_app)


@task
def install_django_haus():
    run_command_on_selected_server(_install_haus_requirements)


@task
def setup_haus_database():
    run_command_on_selected_server(_setup_database)


@task
def start_server():
    run_command_on_selected_server(_start_server)


@task
def create_superuser():
    run_command_on_selected_server(_create_superuser)


@task
def install_nginx():
    run_command_on_selected_server(_install_nginx)


@task
def set_cronjob():
    run_command_on_selected_server(_set_cronjob)


@task
def ssh():
    run_command_on_selected_server(open_shell)


@task
def stop_instance():
    select_instance()
    conn = get_ec2_connection()
    conn.stop_instances(instance_ids=[env.active_instance.id])


@task
def terminate_instance():
    select_instance(state="stopped")
    conn = get_ec2_connection()
    conn.terminate_instances(instance_ids=[env.active_instance.id])


@task
def release_address():
    conn = get_ec2_connection()
    prompt_text = "Please select from the following addresses:\n"
    address_template = " %(ct)d: %(id)s\n"
    addresses = conn.get_all_addresses()
    for idx, address in enumerate(addresses):
        ct = idx + 1
        args = {'ct': ct, 'id': str(address)}
        prompt_text += address_template % args
    prompt_text += "Choose an address: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(addresses) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    addresses[choice - 1].release()

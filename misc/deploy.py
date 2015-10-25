import os.path
import time
import subprocess
import getpass

import paramiko


class Application(object):

    def __init__(self, host: str, name: str, username: str):
        self._username = username
        self._host = host
        self._name = name
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(host, pkey=self._prepare_ssh_key(), username=self._username)
        self._version = str(int(time.time()))

    def process(self):
        self._check()
        self._setup()
        self._deploy()
        self._after_deploy()
        self._promote()
        self._after_promote()

    def close(self):
        self._client.close()

    def _get_app_path(self):
        return os.path.join('/srv', self._name)

    @staticmethod
    def _prepare_ssh_key():
        filename = os.path.expanduser('~/.ssh/id_rsa')
        password = getpass.getpass('Supply password for your SSH key please:')
        return paramiko.RSAKey.from_private_key_file(filename, password)

    def _setup(self):
        app_path = self._get_app_path()
        releases_path = os.path.join(self._get_app_path(), 'releases')
        self._perform_ssh_command('mkdir -p {} && mkdir -p {}'.format(app_path, releases_path))

    def _check(self):
        pass

    def _deploy(self):
        version_path = os.path.join(self._get_app_path(), 'releases', self._version)
        current_dir = os.path.dirname(__file__)
        local_path = os.path.join(current_dir, '..')
        self._perform_ssh_command('mkdir -p {}'.format(version_path))
        subprocess.call("rsync -avz --exclude .git --exclude env -e ssh {} {}@{}:{}".
                        format(local_path, self._username, self._host, version_path), shell=True)

    def _promote(self):
        releases_path = os.path.join(self._get_app_path(), 'releases')
        source = os.path.join(releases_path, self._version)
        destination = os.path.join(releases_path, 'current')
        self._perform_ssh_command('ln -sfn {} {}'.format(source, destination))

    def _perform_ssh_command(self, command: str):
        stdin, stdout, stderr = self._client.exec_command(command)
        for row in stdout:
            print(row)
        err_msg = [row for row in stderr]
        if err_msg:
            raise RuntimeError('\n'.join(err_msg))

    def _after_deploy(self):
        pass

    def _after_promote(self):
        pass

import os.path

from psycopg2 import DatabaseError
from yoyo import read_migrations
from yoyo.connections import exceptions

from misc.deploy import Application
from microservice import components

class Microservice(Application):

    def _check(self):
        current_dir = os.path.dirname(__file__)
        if not os.path.isfile(os.path.join(current_dir, 'config', 'config.yaml')):
            raise RuntimeError('config/config.yaml is missing.')

    def _after_deploy(self):
        version_path = os.path.join(self._get_app_path(), 'releases', self._version)
        self._perform_ssh_command('cd {} && make clean && make'.format(version_path))
        self._do_migrations()

    def _after_promote(self):
        self._perform_ssh_command('./bin/gunicorn restart')

    def _do_migrations(self):
        current_dir = os.path.dirname(__file__)
        migrations_dir = os.path.join(current_dir, 'migrations')
        conn = components.get_psql()
        exceptions.register(DatabaseError)
        migrations = read_migrations(conn, 'pyformat', migrations_dir)
        migrations.to_apply().apply()
        conn.commit()

if __name__ == '__main__':
    print('Deploy started, brace yourselves.')
    microservice = Microservice('127.0.0.1', 'microservice', 'chmelda')
    microservice.process()
    microservice.close()
    print('Done.')
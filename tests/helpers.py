import os.path
import csv
import time
import random

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from microservice import components


class TestDatabase(object):

    def __init__(self):
        self._ddl_conn = components.get_psql()
        self._ddl_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._name = generate_name()
        self._create_database()
        self._conn = components.get_psql(dbname=self._name)

    def use_table(self, table_name: str):
        """

        :param table_name: Name of the table
        :return: None
        """
        self._create_table(table_name)
        self._fill_table(table_name)

    @property
    def connection(self):
        return self._conn

    def _create_database(self):
        with self._ddl_conn.cursor() as cur:
            cur.execute('CREATE DATABASE ' + self._name)

    def _create_table(self, name: str):
        file_name = os.path.join(os.path.dirname(__file__), 'resources', name.capitalize() + '.sql')
        with open(file_name) as sql:
            with self._conn.cursor() as cur:
                cur.execute(sql.read())
            self._conn.commit()

    def _fill_table(self, name):
        file_name = os.path.join(os.path.dirname(__file__), 'resources', name.capitalize() + '.csv')
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile, quotechar='"', delimiter=',', skipinitialspace=True)
            values = list(reader)

        sql, params = self._create_fill_sql_and_params(name, values[0], values[1:])

        with self._conn.cursor() as cur:
            cur.execute(sql, params)
        self._conn.commit()

    @staticmethod
    def _create_fill_sql_and_params(name, columns, rows):
        # TODO: Refactoring
        keys = ['%s'] * len(rows[0])
        sql = 'INSERT INTO ' + name + ' (' + ','.join(columns) + ') VALUES '
        sql += ','.join(['(' + ','.join(keys) + ')'] * len(rows))
        return sql, [item for sublist in rows for item in sublist]

    def close(self):
        self._conn.close()
        with self._ddl_conn.cursor() as cur:
            cur.execute('DROP DATABASE ' + self._name)


def generate_name():
    timestamp = int(time.time())
    random.seed()
    return 'test_{}_{}'.format(timestamp, random.randint(1, 10))

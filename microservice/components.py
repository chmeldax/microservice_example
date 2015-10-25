import redis
import psycopg2

from microservice import config


def get_psql(dbname=None):
    cfg = config.get_config()['psql'].copy()
    if dbname:
        cfg['database'] = dbname
    return psycopg2.connect(**cfg)


def get_redis():
    cfg = config.get_config()['redis'].copy()
    return redis.Redis(decode_responses=True, **cfg)


def get_riemann():
    return

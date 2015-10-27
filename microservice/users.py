import psycopg2
import psycopg2.extras
import json

from microservice import components

REDIS_KEY = 'microservice_cached_users_all'


def get_all() -> list:
    """
    Gets list of all users in the DB.
    If any error occurs when pulling data from the DB, we use cached data in the Redis.
    If even that fails, exception will be raised.
    :return: list
    """
    try:
        db = components.get_psql()
        redis = components.get_redis()
        result = _get_all_from_db(db)
        _save_all_to_redis(redis, result)
        return result
    except psycopg2.DatabaseError:
        return _get_all_from_redis(components.get_redis())


def _get_all_from_db(db):
    with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT username FROM users ORDER BY users.id')
        return [row['username'] for row in cursor.fetchall()]


def _get_all_from_redis(redis):
    cached_response = redis.get(REDIS_KEY)
    return json.loads(cached_response)


def _save_all_to_redis(redis, users: list):
    cached_response = json.dumps(users)
    redis.set(REDIS_KEY, cached_response)

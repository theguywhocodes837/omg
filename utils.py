from redis import Redis


from decouple import config


def redis_connection():
    conn = Redis(host=config("REDIS_HOST"))
    return conn

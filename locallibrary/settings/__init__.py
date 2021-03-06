from .common import *

# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
# import environ
#
#
# environ.Env.read_env()
# env = environ.Env()
# print(list(env))
from decouple import config

if config('DEBUG', default=False, cast=bool):
    from .development import *
else:
    from .production import *
    # Heroku: Update database configuration from $DATABASE_URL.
    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=500, require_ssl=True)
    DATABASES['default'] = db_from_env

# from .production import *
# # Heroku: Update database configuration from $DATABASE_URL.
# import dj_database_url
#
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)
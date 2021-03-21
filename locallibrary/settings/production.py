import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

from decouple import config
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['shrouded-shelf-78516.herokuapp.com', '0.0.0.0', 'localhost']

# 'shrouded-shelf-78516.herokuapp.com',
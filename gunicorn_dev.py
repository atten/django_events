import os

bind = 'localhost:43210'

workers = os.environ.get('GUNICORN_WORKERS', 2)
worker_class = 'sync'

reload = True
preload_app = True
raw_env = [
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]

timeout = os.environ.get('GUNICORN_TIMEOUT', 10)

accesslog = '-'
errorlog = '-'

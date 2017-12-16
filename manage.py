#!/usr/bin/env python
import os
import sys


def run_gunicorn(is_production: bool, ensure_connection_alive: bool=False):
    from django_events.wsgi import application  # noqa
    from django_docker_helpers.management import run_gunicorn  # noqa

    if ensure_connection_alive:
        ensure_connections()

    gunicorn_module_name = 'gunicorn_prod' if is_production else 'gunicorn_dev'
    run_gunicorn(application, gunicorn_module_name=gunicorn_module_name)


def ensure_connections():
    from django_docker_helpers.db import ensure_databases_alive, ensure_caches_alive, migrate  # noqa

    ensure_databases_alive(100)
    ensure_caches_alive(100)
    migrate()


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_events.settings')

    IS_PRODUCTION = bool(int(os.environ.get('PRODUCTION', 0) or 0))
    IS_DOCKERIZED = bool(int(os.environ.get('DOCKERIZED', 0) or 0))

    if IS_DOCKERIZED:
        ensure_connections()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'runuwsgi':
            from django.conf import settings

            os.environ.setdefault('PORT', str(settings.COMMON_BASE_PORT))
            # WARNING: production unsafe security option! DO NOT USE IT ON PRODUCTION
            # we treat an empty string and non-falsy values as the enabled static-safe option
            safe = getattr(settings, 'UWSGI_STATIC_SAFE', None)
            if safe or safe == '':
                os.environ.setdefault('UWSGI_STATIC_SAFE', str(settings.UWSGI_STATIC_SAFE))

        if sys.argv[1] == 'gunicorn':
            run_gunicorn(IS_PRODUCTION)
            exit()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

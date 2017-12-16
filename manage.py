#!/usr/bin/env python
import os
import sys

from django.core.exceptions import ImproperlyConfigured


def run_gunicorn(is_production: bool):
    from django_events.wsgi import application  # noqa
    from django_docker_helpers.management import run_gunicorn  # noqa

    gunicorn_module_name = 'gunicorn_prod' if is_production else 'gunicorn_dev'
    run_gunicorn(application, gunicorn_module_name=gunicorn_module_name)


def _prepare():
    from django_docker_helpers.db import ensure_databases_alive, ensure_caches_alive, migrate  # noqa
    from django_docker_helpers.files import collect_static
    from django_docker_helpers.management import create_admin

    collect_static()
    ensure_databases_alive(100)
    ensure_caches_alive(100)
    migrate()
    create_admin()


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_events.settings')

    IS_PRODUCTION = bool(int(os.environ.get('PRODUCTION', 0) or 0))
    IS_DOCKERIZED = bool(int(os.environ.get('DOCKERIZED', 0) or 0))

    if IS_DOCKERIZED:
        _prepare()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'runuwsgi':
            from django.conf import settings

            os.environ.setdefault('PORT', str(settings.COMMON_BASE_PORT))
            safe = getattr(settings, 'UWSGI_STATIC_SAFE', None)
            if safe or safe == '':
                if IS_PRODUCTION:
                    raise ImproperlyConfigured(r"""
                        WARNING: UWSGI_STATIC_SAFE is the unsafe security option! DO NOT USE IT ON PRODUCTION!!! 
                        (We treat an empty string and non-falsy values as 'enable static-safe option')""")

                os.environ.setdefault('UWSGI_STATIC_SAFE', str(settings.UWSGI_STATIC_SAFE))

        if sys.argv[1] == 'gunicorn':
            run_gunicorn(IS_PRODUCTION)
            exit()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

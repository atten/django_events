#!/usr/bin/env python
import os
import sys


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_events.settings')

    IS_PRODUCTION = bool(int(os.environ.get('PRODUCTION', 0) or 0))
    IS_DOCKERIZED = bool(int(os.environ.get('DOCKERIZED', 0) or 0))

    if IS_DOCKERIZED:
        from cli.run_ensure_connections import ensure_connections
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
            # ./manage.py gunicorn
            from cli.run_gunicorn import run_gunicorn
            run_gunicorn(IS_PRODUCTION)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

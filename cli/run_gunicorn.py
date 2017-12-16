

def run_gunicorn(is_production: bool, ensure_connection_alive: bool=False):
    from django_events.wsgi import application  # noqa
    from django_docker_helpers.management import run_gunicorn  # noqa

    if ensure_connection_alive:
        from cli.run_ensure_connections import ensure_connections
        ensure_connections()

    gunicorn_module_name = 'gunicorn_prod' if is_production else 'gunicorn_dev'
    run_gunicorn(application, gunicorn_module_name=gunicorn_module_name)

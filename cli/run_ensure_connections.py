

def ensure_connections():
    from django_docker_helpers.db import ensure_databases_alive, ensure_caches_alive, migrate  # noqa

    ensure_databases_alive(100)
    ensure_caches_alive(100)
    migrate()

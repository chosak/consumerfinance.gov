import os

from psycogreen.gevent import patch_psycopg


def on_starting(server):
    """Patch psycopg2 for gevent workers."""
    patch_psycopg()


# Server socket
bind = ":8000"

# Worker processes
# Default to 1 worker for local development (allows debugging with pdb)
# For production, set GUNICORN_WORKERS based on CPU resources
workers = int(os.environ.get("GUNICORN_WORKERS", "1"))

# Worker class
# - "sync" for development (better for debugging with pdb/breakpoint)
# - "gevent" for production (better concurrency and performance)
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "sync")

# Worker connections (only relevant for gevent/eventlet workers)
worker_connections = int(os.environ.get("GUNICORN_WORKER_CONNECTIONS", "30"))

# Worker timeout
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "0"))

# Worker lifecycle - restart workers after N requests to prevent memory leaks
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(
    os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "100")
)

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Auto-reload on code changes (development only)
# In production, this should be disabled
reload = os.environ.get("GUNICORN_RELOAD", "true").lower() == "true"

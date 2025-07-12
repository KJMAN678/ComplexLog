#!/bin/sh
uv run app/manage.py migrate
uv run app/manage.py createsuperuser --noinput || true
uv run app/manage.py sync_blogs_to_opensearch || echo "Warning: Failed to sync blogs to OpenSearch during startup"
uv run app/manage.py runserver 0.0.0.0:8000

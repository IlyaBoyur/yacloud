#!/bin/sh
alembic current
alembic upgrade head
exec "$@"
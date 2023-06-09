#!/bin/bash

# Waiting for database to become live
sleep 20

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Start server
echo "Starting server"

#TODO: Due to hypercorn port already in use error caching data commands faile to execute.
python manage.py cacheuserdata
python manage.py cachedepartmentdata
python manage.py cachedesignationdata
python manage.py cacheteamdata
python manage.py cacheprojectdata
#python manage.py remove_stale_contenttypes --noinput
hypercorn tms.wsgi:application --workers 1 --bind 0.0.0.0:8020

#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Start server
echo "Starting server"

python manage.py cacheuserdata
python manage.py cachedepartmentdata
python manage.py cachedesignationdata
python manage.py cacheteamdata
python manage.py cacheprojectdata
python manage.py runserver --force-color
#python manage.py remove_stale_contenttypes --noinput

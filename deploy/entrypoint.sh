#! /bin/bash

cd /src/ || exit

# echo "PIP INSTALLATION" && pip install -r requirements.txt

echo "MIGRATING" && python manage.py migrate

# Initadmin runs successfully for the first time only when
# there is no user data -> hence first deployment

echo "INITADMIN" && python manage.py initadmin

echo "COLLECT STATIC" && python manage.py collectstatic --noinput

exec "$@"

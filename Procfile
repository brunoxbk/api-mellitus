web: poetry run gunicorn mellitus.wsgi:application

release: sh -c 'poetry run python manage.py migrate --noinput && poetry run python manage.py collectstatic --noinput --clear'
web: poetry run gunicorn mellitus.wsgi:application

release: sh -c 'poetry run python migrate --noinput && poetry run python manage.py collectstatic --noinput --clear'
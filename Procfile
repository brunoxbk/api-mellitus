web: poetry run gunicorn mellitus.wsgi:application

release: poetry run python migrate --noinput && poetry run python manage.py collectstatic --noinput --clear
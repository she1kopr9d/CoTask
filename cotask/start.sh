#!/bin/bash

# Применяем миграции
python manage.py migrate

# Собираем статику с игнорированием ошибок
python manage.py collectstatic --noinput --clear

# Запускаем Gunicorn
exec gunicorn cotask.wsgi:application --bind 0.0.0.0:8000
#!/bin/bash
echo "🚀 Запуск сборки..."
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
echo "✅ Сборка завершена!"

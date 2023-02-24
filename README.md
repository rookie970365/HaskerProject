# Hasker: Poor Man's Stackoverflow



Django приложение с API, реализующее Q&A сайт, аналог stackoverflow.com

## Установка среды разработки
*git clone https://github.com/rookie970365/HaskerProject.git*

### Cоздание виртуального окружения:
*cd hasker*

*python -m venv venv*

*source venv/bin/activate*  

### Установка зависимостей:
*pip install -r requirements.txt*

### Запуск сервера разработки:
*python manage.py migrate*

*python manage.py runserver*

### Тестирование:
*python manage.py test*

### Документация по API:
/api/v1/swagger

/api/v1/redoc

## Развертываниe проекта в конфигурации django + nginx + gunicorn + postgresql с помощью docker
*git clone https://github.com/rookie970365/HaskerProject.git*

*docker-compose build*

*docker compose up -d*

*docker-compose exec web python manage.py migrate*

Адрес: http://localhost


## Требования
- Python 3.10
- Django 4.1
- Django REST framework 3.14



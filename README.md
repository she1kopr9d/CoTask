# CoTask - Совершенствуйся вместе!

## Описание проекта | Project Description

CoTask - это платформа для совместной работы и саморазвития, где пользователи могут создавать и выполнять задачи, отслеживать прогресс и взаимодействовать с другими участниками.

CoTask is a collaborative platform for personal development where users can create and complete tasks, track progress, and interact with other participants.

## Технологии | Technologies

- Python/Django
- PostgreSQL
- Docker
- Nginx
- Gunicorn

## Требования | Requirements

- Docker
- Docker Compose
- Python 3.8+
- Git

## Установка и запуск | Installation and Running

1. Клонируйте репозиторий:
   ```bash
   git clone [repository-url]
   cd CoTask
   ```

2. Создайте файл .env в корневой директории:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://postgres:postgres@db:5432/notification_db
   ```

3. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Примените миграции:
   ```bash
   docker-compose exec site python manage.py migrate
   ```

5. Создайте суперпользователя:
   ```bash
   docker-compose exec site python manage.py createsuperuser
   ```

## Структура проекта | Project Structure

```
CoTask/
├── cotask/           # Основное приложение Django
├── nginx/           # Конфигурация Nginx
├── docker-compose.yml
└── README.md
```

## Разработка | Development

Для локальной разработки:

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   .\venv\Scripts\activate  # Windows
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Лицензия | License

[Укажите лицензию проекта]

## Контакты | Contacts

[Укажите контактную информацию]
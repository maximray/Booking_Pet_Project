# My_booking - Сервис бронирования отелей

![Tech Stack](https://img.shields.io/badge/Python-3.9-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.92.0-green) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue) ![Docker](https://img.shields.io/badge/Docker-20.10-orange)

Сервис для бронирования отелей с асинхронным API, мониторингом и администрированием.

## 🛠 Технологии

| Категория       | Технологии                                                                 |
|-----------------|----------------------------------------------------------------------------|
| Backend         | Python 3.9, FastAPI 0.92.0, Uvicorn, Gunicorn                             |
| Базы данных     | PostgreSQL, SQLAlchemy 2.0.4, Asyncpg, Alembic                            |
| Аутентификация  | JWT, Cookies                                                              |
| Асинхронность   | Anyio, Celery 5.2.7                                                       |
| Инфраструктура  | Docker, Redis 4.5.2, Prometheus, Grafana, Sentry                          |
| Дополнительно   | CORS, Flower (мониторинг Celery), fastapi-cache2 0.2.1                    |

## 🌟 Функционал

### Для пользователей
- 🔐 Кастомная регистрация и аутентификация (JWT + Cookies)
- 🏨 Поиск отелей по локации и датам
- 📅 Бронирование номеров с email-подтверждением (Celery)
- 📊 Просмотр своих бронирований и отмена броней
- 🖼 Загрузка и просмотр изображений отелей

### Для администраторов
- ⚙️ Админ-панель
- 📊 Мониторинг ошибок (Sentry)
- 📈 Сбор метрик (Prometheus) и визуализация (Grafana)
- 📝 Логирование (кастомный логгер)

### Системные особенности
- 🚀 Асинхронные запросы
- 🐳 Готовые Docker-контейнеры
- 🔄 Кеширование (Redis)
- 📚 API версионирование

## 🚀 Запуск проекта

### Локально (с Docker)
1. Установите [Docker](https://docs.docker.com/get-docker/) и [Redis](https://redis.io/docs/getting-started/)
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/maximray/Booking_Pet_Project
   cd my_booking

3. Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
Команды для Windows:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
Перейти в директорию app:
   ```bash
   cd /app
   ```
Создать файл .env по образцу:
   ```bash
   cp .env-local-example .env
   ```
Установить зависимости из файла requirements.txt:
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

Для создания миграций выполнить команду:
   ```bash
   alembic init migrations
   ```
В папку migrations в env файл вставьте следующий код:
```python
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.bookings.models import Booking
from app.config import settings
from app.database.db import Base
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User


config = context.config
config.set_main_option('sqlalchemy.url', f'{settings.DATABASE_URL}?async_fallback=True')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```
Инициализировать БД:
   ```bash
    alembic revision --autogenerate -m "comment"
   ```
Применить миграцию:
```bash
    alembic upgrade head
```
Запустить проект:
```bash
    uvicorn app.main:app --reload
```
Запустить Redis:
```bash
    redis-server.exe
    redis-cli.exe
```
Запустить Celery:
```bash
    celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
```
Запустить Flower:
```bash
    celery -A app.tasks.tasks:celery flower
```
# Запуск в контейнерах Docker
Находясь в главной директории проекта
Создать файл .env-docker по образцу:
   ```bash
   cp .env-docker-example .env-docker
```
Запустить проект:
```bash
    docker-compose up -d --build
```
Примеры некоторых запросов API
Регистрация пользователя:
```
   POST /users/register
```
Получение данных своей учетной записи:
```
   GET /users/me
```
Добавление бронирование:
```
   POST /bookings
```
Получение списка своих бронирований:
```
   GET /bookings
```
Получение списка отелей по нужной локации:
```
   GET /hotels/{location}
```
Получение списка доступных для бронирования комнат по заданным параметрам:
```
   GET /hotels/{hotel_id}/rooms
```
# Полный список запросов API находится в документации

    

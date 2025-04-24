# Сервис My_booking
# Описание
Cервис бронирования отелей.Пользователи могут забронировать необходимый тип номера в отеле на определённую дату.Реализована загрузка изображений отелей.Существует возможность просмотра выборки доступных для бронирования отелей по месту локации в виде обычной страницы.Реализовано логирование, мониторинг ошибок, сбор метрик и их визуализация.Подготовлены тестовые данные для заполнения БД.Используется асинхронный подход к запросам.Проект подготовлен как для локального развертывания, так и в Docker-контейнерах.
# Функционал
Кастомная регистрация пользователей.
Аутентификация реализована с помощью куков и JWT-токена.
У неаутентифицированных пользователей доступ к API только на уровне чтения.
Создание объектов разрешено только аутентифицированным пользователям.
Возможность получения подробной информации о себе.
Загрузка тестовых данных в БД.
Возможность забронированить комнату отеля, получить список всех своих бронирований и отменить(удалить) свою бронь.
Отправка email с подтверждением бронирования пользователю посредством Celery.
Поиск и получение списка всех отелей по заданным параметрам местоположения на определенную дату.
Возможность получить список всех отелей без исключения и информацию по каждому из них отдельно.
Возможность получить список всех доступных для бронирования комнат конкретного отеля на определенную дату.
Возможность получить список всех типов комнат и информацию по каждой из них отдельно.\n
Загрузка файлов с изображениями для отелей и их обработка при загрузке с помощью Celery.
Возможность просмотра выборки доступных для бронирования отелей по месту локации в виде обычной страницы.
Возможность администрирования сервиса.
Версионирование API.
Кеширование/брокер задач с помощью Redis.
Логирование посредством кастомного логгера.
Мониторинг ошибок с помощью Sentry.
Сбор метрик с помощью Prometheus.
Визуализация метрик посредством Grafana.
Возможность развернуть проект в Docker-контейнерах.
# Локально документация доступна по адресу: 
http://localhost:8000/v1/docs/
# В контейнерах Docker документация доступна по адресу:
http://localhost:7777/v1/docs/
# Технологии
Python 3.9
FastAPI 0.92.0
fastapi-cache2 0.2.1
Асинхронность
Anyio
Cookies
JWT
Alembic
SQLAlchemy 2.0.4
Docker
PostgreSQL
Asyncpg
CORS
Redis 4.5.2
Celery 5.2.7
Flower
Sentry
Prometheus
Grafana
Uvicorn
Gunicorn
# Локальный запуск проекта
Предварительно необходимо установить Docker и Redis для вашей системы.

Склонировать репозиторий:

   git clone <название репозитория>
Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

   python3 -m venv env
   source env/bin/activate
Команды для Windows:

   python -m venv venv
   source venv/Scripts/activate
Перейти в директорию app:
   cd /app
Создать файл .env по образцу:
   cp .env-local-example .env
Установить зависимости из файла requirements.txt:
   cd ..
   pip install -r requirements.txt
Для создания миграций выполнить команду:
   alembic init migrations
В папку migrations в env файл вставьте следующий код:
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
Инициализировать БД:
    alembic revision --autogenerate -m "comment"  
Применить миграцию:
    alembic upgrade head 
Запустить проект:
    uvicorn app.main:app --reload   
Запустить Redis:
    redis-server.exe
    redis-cli.exe
Запустить Celery:
    celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
Запустить Flower:
    celery -A app.tasks.tasks:celery flower
Запуск в контейнерах Docker
Находясь в главной директории проекта:

Создать файл .env-docker по образцу:

   cp .env-docker-example .env-docker
Запустить проект:
    docker-compose up -d --build  
# Примеры некоторых запросов API
Регистрация пользователя:

   POST /users/register
Получение данных своей учетной записи:

   GET /users/me 
Добавление бронирование:

   POST /bookings
Получение списка своих бронирований:

   GET /bookings
Получение списка отелей по нужной локации:

   GET /hotels/{location}
Получение списка доступных для бронирования комнат по заданным параметрам:

   GET /hotels/{hotel_id}/rooms
# Полный список запросов API находится в документации
# Автор
https://github.com/maximray

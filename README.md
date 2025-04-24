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
   git clone https://github.com/your-repo/my_booking.git
   cd my_booking

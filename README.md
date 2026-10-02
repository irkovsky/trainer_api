# Trainer API

Backend для фитнес-тренера. Клиенты загружают медицинские анализы, тренер просматривает их и отслеживает прогресс.

## Стек

- Python 3.11
- Django 5.x
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- PostgreSQL / SQLite
- django-filter
- pytest + pytest-django

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/username/trainer_api.git
cd trainer_api
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Применить миграции

```bash
python manage.py migrate
```

### 5. Создать суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

Сервер доступен по адресу: `http://127.0.0.1:8000/`

## Эндпоинты

### Аутентификация

| Метод | URL | Описание |
| :--- | :--- | :--- |
| POST | `/api/register/` | Регистрация нового пользователя |
| POST | `/api/token/` | Получить JWT-токен (access + refresh) |
| POST | `/api/token/refresh/` | Обновить access-токен |

### Анализы

| Метод | URL | Описание |
| :--- | :--- | :--- |
| GET | `/api/analyses/` | Список анализов |
| POST | `/api/analyses/` | Создать анализ |
| GET | `/api/analyses/{id}/` | Получить один анализ |
| PATCH | `/api/analyses/{id}/` | Обновить анализ |
| DELETE | `/api/analyses/{id}/` | Удалить анализ |

### Фильтры и пагинация

```
GET /api/analyses/?date_after=2026-01-01&date_before=2026-12-31
GET /api/analyses/?title=кровь
GET /api/analyses/?page=1&page_size=10
```

## Роли и права

| Роль | Что может |
| :--- | :--- |
| **client** | Создавать анализы, видеть только свои |
| **admin** | Видеть все анализы, удалять любые |

## Примеры запросов

### Регистрация

```http
POST /api/register/
Content-Type: application/json

{
    "username": "client1",
    "password": "client12345",
    "role": "client"
}
```

### Получить токен

```http
POST /api/token/
Content-Type: application/json

{
    "username": "client1",
    "password": "client12345"
}
```

### Создать анализ

```http
POST /api/analyses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "date": "2026-10-02",
    "title": "Общий анализ крови",
    "data": {
        "hemoglobin": 140,
        "leukocytes": 6.5
    }
}
```

## Тесты

Запуск тестов:

```bash
pytest
```

Запуск с покрытием:

```bash
pytest --cov=api --cov-report=term-missing
```

**Текущее покрытие:** 99%.

## Структура проекта

```
trainer_api/
├── api/
│   ├── migrations/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_analyses.py
│   │   └── test_permissions.py
│   ├── admin.py
│   ├── filters.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── pytest.ini
├── manage.py
└── requirements.txt
```

## Лицензия

MIT
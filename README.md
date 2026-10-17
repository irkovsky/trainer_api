# Trainer API

Backend для фитнес-тренера: клиенты загружают медицинские анализы, тренер назначает тренировки и отслеживает прогресс.

**Обновлено:** 17.10.2026

---

## Статус проекта

### ✅ MVP №1: Анализы
- API (DRF): CRUD, JWT, права, фильтры, пагинация
- Веб-интерфейс: список, создание, просмотр, редактирование, удаление
- Тесты: 14 passed, 99% покрытие

### ✅ MVP №2: Тренировки
- API: CRUD, права (только админ создаёт)
- Веб-интерфейс: список, создание, просмотр, редактирование, удаление
- Тесты: 5 passed

### ✅ MVP №3: Прогресс по упражнениям
- Модели `Exercise` и `ExerciseSet`
- API: CRUD для упражнений и подходов (RPE, заметки)
- Веб-интерфейс: упражнения внутри тренировки, отметка подходов
- ⏳ Тесты: запланировано

### 🔜 В планах
- **MVP №4**: Динамика анализов + замеры тела (вес, обхваты)
- **MVP №5**: AI-функции (описание анализов, голосовой ввод, чат-бот)
- **Финализация**: деплой на VPS, домен, SSL

---

## Стек

- **Backend:** Python 3.11, Django 5.x, Django REST Framework
- **Аутентификация:** JWT (`djangorestframework-simplejwt`) + сессии для веба
- **База данных:** PostgreSQL (в разработке — SQLite)
- **Фильтрация:** `django-filter`
- **Тесты:** `pytest`, `pytest-django`, `pytest-cov`
- **Фронтенд:** Django Templates
- **Деплой (план):** Nginx, Gunicorn, VPS

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<username>/trainer_api.git
cd trainer_api

# 2. Виртуальное окружение
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Зависимости
pip install -r requirements.txt

# 4. Миграции
python manage.py migrate

# 5. Суперпользователь
python manage.py createsuperuser

# 6. Запуск
python manage.py runserver
```

---

## API-эндпоинты

### Аутентификация

| Метод | URL | Описание |
| :--- | :--- | :--- |
| POST | `/api/register/` | Регистрация |
| POST | `/api/token/` | Получить JWT-токен |
| POST | `/api/token/refresh/` | Обновить access-токен |

### Анализы

| Метод | URL | Описание |
| :--- | :--- | :--- |
| GET | `/api/analyses/` | Список анализов |
| POST | `/api/analyses/` | Создать анализ |
| GET | `/api/analyses/{id}/` | Один анализ |
| PATCH | `/api/analyses/{id}/` | Обновить |
| DELETE | `/api/analyses/{id}/` | Удалить |

### Тренировки

| Метод | URL | Описание |
| :--- | :--- | :--- |
| GET | `/api/workouts/` | Список тренировок |
| POST | `/api/workouts/` | Создать тренировку (админ) |
| GET | `/api/workouts/{id}/` | Одна тренировка |
| PATCH | `/api/workouts/{id}/` | Обновить (админ) |
| DELETE | `/api/workouts/{id}/` | Удалить (админ) |

### Упражнения

| Метод | URL | Описание |
| :--- | :--- | :--- |
| GET | `/api/exercises/` | Список упражнений |
| POST | `/api/exercises/` | Создать упражнение (админ) |
| GET | `/api/exercises/{id}/` | Одно упражнение |
| PATCH | `/api/exercises/{id}/` | Обновить (админ) |
| DELETE | `/api/exercises/{id}/` | Удалить (админ) |

### Подходы

| Метод | URL | Описание |
| :--- | :--- | :--- |
| GET | `/api/exercise-sets/` | Список подходов |
| POST | `/api/exercise-sets/` | Отметить подход |
| GET | `/api/exercise-sets/{id}/` | Один подход |
| PATCH | `/api/exercise-sets/{id}/` | Обновить |
| DELETE | `/api/exercise-sets/{id}/` | Удалить |

### Фильтры и пагинация

- `?search=...` — поиск по названию/описанию
- `?status=OPEN` — фильтр по статусу (для анализов)
- `?date_after=YYYY-MM-DD&date_before=YYYY-MM-DD` — диапазон дат
- `?page=1&page_size=10` — пагинация

---

## Веб-страницы

| URL | Описание |
| :--- | :--- |
| `/register/` | Регистрация |
| `/login/` | Логин |
| `/logout/` | Выход |
| `/analyses/` | Список анализов |
| `/analyses/create/` | Создание анализа |
| `/analyses/<pk>/` | Просмотр анализа |
| `/analyses/<pk>/update/` | Редактирование |
| `/analyses/<pk>/delete/` | Удаление |
| `/workouts/` | Список тренировок |
| `/workouts/create/` | Создание тренировки |
| `/workouts/<pk>/` | Просмотр тренировки + упражнения |
| `/workouts/<pk>/update/` | Редактирование |
| `/workouts/<pk>/delete/` | Удаление |
| `/workouts/<workout_pk>/exercises/create/` | Создание упражнения |
| `/exercises/<pk>/update/` | Редактирование упражнения |
| `/exercises/<pk>/delete/` | Удаление упражнения |
| `/exercises/<exercise_pk>/sets/create/` | Отметка подхода |
| `/exercise-sets/<pk>/delete/` | Удаление подхода |

---

## Тесты

```bash
# Все тесты
pytest

# Покрытие
pytest --cov=api --cov-report=term-missing

# Только workouts
pytest api/tests/test_workouts.py -v
```

**Покрытие:** 99% (MVP №1), 5 тестов для тренировок. Тесты для MVP №3 — в планах.

---

## Структура проекта

```
trainer_api/
├── api/
│   ├── migrations/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_analyses.py
│   │   ├── test_auth.py
│   │   ├── test_permissions.py
│   │   └── test_workouts.py
│   ├── filters.py
│   ├── forms.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── views_web.py
├── config/
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── analyses/
│   ├── auth/
│   └── workouts/
├── .gitignore
├── manage.py
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Лицензия

MIT
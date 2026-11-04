# Blog Project

Django-проект блога с постами, комментариями, авторизацией и разграничением прав.

## Особенности реализации

- **Посты**: создание, просмотр, редактирование и удаление (CRUD).
- **Комментарии**: добавление только авторизованными пользователями; имя, email и автор подставляются автоматически.
- **Права доступа**: редактировать и удалять пост может только его автор; при попытке доступа чужого пользователя возвращается ошибка `403 Forbidden`.
- **Авторизация**: вход, выход и регистрация новых пользователей.
- **Тесты**: 11 unit-тестов, покрывающих модели, views и права доступа.
- **Production-ready**: разделение настроек по средам, Docker, Gunicorn + Nginx, переменные окружения.

## Стек технологий

- Python 3.13
- Django 5.2
- SQLite (dev) / PostgreSQL (prod)
- Gunicorn + Nginx (prod)
- Docker и docker-compose
- WhiteNoise

## Запуск в режиме разработки

1. **Создайте и активируйте виртуальное окружение:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Установите зависимости:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Создайте файл переменных окружения:**

   ```powershell
   copy .env.example .env
   ```

   Заполните `SECRET_KEY` — он обязателен и читается из переменных окружения.

4. **Примените миграции:**

   ```powershell
   python manage.py makemigrations blog_app
   python manage.py migrate
   ```

5. **Создайте суперпользователя:**

   ```powershell
   python manage.py createsuperuser
   ```

6. **Запустите сервер:**

   ```powershell
   python manage.py runserver
   ```

   Проект доступен по адресу: `http://127.0.0.1:8000/`

## Запуск в продакшене (Docker)

1. **Заполните `.env`** реальными значениями (`SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, пароль БД).

2. **Соберите и запустите контейнеры:**

   ```bash
   docker compose up --build -d
   ```

   Поднимаются три сервиса: `db` (PostgreSQL), `web` (Django + Gunicorn) и `nginx` (прокси + статика).

3. **Создайте суперпользователя в контейнере:**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

4. **Остановка:**

   ```bash
   docker compose down
   ```

## Настройки по средам

- **dev** (`blog_project/settings/dev.py`): SQLite, `DEBUG=True`, локальные хосты.
- **prod** (`blog_project/settings/prod.py`): PostgreSQL, `DEBUG=False`, `SECURE_SSL_REDIRECT`, HSTS, secure-куки.

Среда выбирается через переменную `DJANGO_SETTINGS_MODULE` (по умолчанию dev, в Docker — prod).

## Тестирование

Запуск всех тестов:

```powershell
python manage.py test
```
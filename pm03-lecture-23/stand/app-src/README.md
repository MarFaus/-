# Cloud Application (учебный стенд)
Установка: python -m venv .venv && .venv/bin/pip install -r requirements.txt
Миграции: alembic upgrade head
Запуск: uvicorn app.main:app --host 127.0.0.1 --port 8000

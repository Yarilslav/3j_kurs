# Praktichni 3j Kurs

## Швидкий старт
```powershell
py -m poetry install
py -m poetry run praktychni-3j-kurs
```

## FastAPI
Запуск локального сервера:
```powershell
poetry run praktychni-3j-kurs
```
Після запуску відкрити в браузері:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

## Тести
Запуск тестів у Docker з окремою PostgreSQL test DB:
```powershell
docker compose --profile test up --build tests
```

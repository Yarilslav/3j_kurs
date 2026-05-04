# Tea House “Asahi” Web Application (茶屋朝日)

## Опис проєкту
Веб-додаток для чайного дому “Асахі”, який дозволяє користувачам 
переглядати каталог товарів, оформлювати замовлення та бронювати місця.  
Персонал може керувати замовленнями, контентом та роботою закладу через API.

Система побудована як backend API на FastAPI з використанням PostgreSQL
як основної бази даних та Docker Compose для контейнеризації сервісів.

---

## Швидкий старт
```powershell
docker compose up --build
```




## FastAPI
Запуск локального сервера:
```powershell
poetry run praktychni-3j-kurs
```
Після запуску відкрити в браузері:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/metrics/

## Тести
Запуск тестів у Docker з окремою PostgreSQL test DB:
```powershell
docker compose --profile test up --build tests
```

## Prometheus
Запуск моніторингу разом із застосунком:
```powershell
docker compose up -d db alembic app prometheus grafana
```

Після запуску Prometheus доступний на:
- http://127.0.0.1:9090/

Grafana доступна на:
- http://127.0.0.1:3000/

Стандартний логін береться з `.env.grafana` через `GF_SECURITY_ADMIN_USER` і `GF_SECURITY_ADMIN_PASSWORD`.
Після входу буде доступний готовий dashboard:
- `Praktychni / FastAPI Overview`

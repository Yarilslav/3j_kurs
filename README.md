# Tea House "Asahi" Web Application

## Опис проекту

Веб-додаток для чайного дому "Асахі", який дозволяє переглядати каталог товарів, оформлювати замовлення та бронювати місця. Система також має базові інструменти для керування товарами, замовленнями та бронюваннями.

## Архітектура

- Backend: FastAPI
- Database: PostgreSQL
- Frontend: React + Vite
- Migrations: Alembic
- Контейнеризація: Docker / Docker Compose
- Monitoring: Prometheus + Grafana

## Локальний запуск

1. Створіть локальний env-файл:

```bash
cp .env.example .env
```

2. Для навчального локального запуску можна використати значення з прикладу, але секрети у `.env` мають бути змінені перед production-деплойментом.

3. Запустіть проект:

```bash
docker compose up --build
```

Доступ до сервісів:

- Backend Swagger: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/healthz
- Readiness check: http://127.0.0.1:8000/readyz
- Metrics: http://127.0.0.1:8000/metrics
- Frontend: http://127.0.0.1:5173
- Prometheus: http://127.0.0.1:9090
- Grafana: http://127.0.0.1:3000

Для цього проекту локальний `docker compose` є основним і рекомендованим способом запуску.

Для спрощення локального стенду контейнер `db` налаштований з `POSTGRES_HOST_AUTH_METHOD=trust`, тому підключення між контейнерами в docker-мережі не вимагають окремої перевірки пароля. Це зручно для навчального проекту локально, але не підходить для production.

## Тести

```bash
docker compose --profile test up --build --abort-on-container-exit tests
```

## Основні API endpoint-и

- Auth: `POST /register`, `POST /login`, `GET /me`
- Users: `GET /users/`, `POST /users/`, `PUT /users/{user_id}`, `DELETE /users/{user_id}`, `PATCH /users/by-login/{login}/role`
- Products: `GET /products/`, `GET /products/{id}`, `POST /products/`, `PUT /products/{id}`, `DELETE /products/{id}`
- Orders: `POST /orders/`, `GET /orders/`, `PATCH /orders/{order_id}/status`
- Reservations: `POST /reservations/`, `GET /reservations/`, `PATCH /reservations/{reservation_id}/status`

## Frontend

Frontend реалізовано як low-fi прототип на React + Vite.

Маршрути frontend:

- `/` - головна сторінка
- `/auth` - сторінка входу та реєстрації
- `/catalog` - каталог товарів
- `/catalog/:id` - сторінка окремого товару
- `/booking` - сторінка бронювання
- `/admin` - демонстраційна admin-панель

Для деплойменту frontend на S3/CloudFront, Amplify або Render встановіть:

```env
VITE_API_URL=https://your-api-domain.example
VITE_API_BASE_URL=https://your-api-domain.example
```

і зберіть статичні файли:

```bash
cd frontend
npm ci
npm run build
```

## Додаткові матеріали

У папці `docs/` знаходяться user flow, flow diagram та low-fi wireframes сторінок.

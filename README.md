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

## Тести

```bash
docker compose --profile test up --build --abort-on-container-exit tests
```

## Підготовка до AWS

Рекомендований навчальний шлях деплойменту:

- Backend: Docker image у Amazon ECR, запуск через ECS Fargate, Elastic Beanstalk Docker або App Runner.
- Database: Amazon RDS PostgreSQL.
- Frontend: окремо через S3 + CloudFront або AWS Amplify.
- Секрети: AWS Secrets Manager, Parameter Store або environment variables сервісу деплойменту.
- Health check для load balancer: `/healthz`.
- Readiness check з перевіркою БД: `/readyz`.

Мінімальні production-змінні:

```env
ENVIRONMENT=production
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=false
DATABASE_URL=postgresql+psycopg_async://USER:PASSWORD@RDS_HOST:5432/DB_NAME
POSTGRES_DB=DB_NAME
POSTGRES_USER=USER
POSTGRES_PASSWORD=PASSWORD
SECRET_KEY=generate-a-random-32-plus-character-secret
FRONTEND_CORS_ORIGINS=https://your-frontend-domain.example
ADMIN_BOOTSTRAP_ENABLED=false
RUN_MIGRATIONS=false
```

Для першого деплойменту можна виконати міграції окремою ECS task або тимчасово встановити:

```env
RUN_MIGRATIONS=true
```

Не залишайте `RUN_MIGRATIONS=true` як постійну поведінку для кількох одночасних інстансів.

## Production smoke test локально

Скопіюйте `.env.example` у `.env`, змініть `SECRET_KEY`, `POSTGRES_PASSWORD`, `ADMIN_PASSWORD`, після чого:

```bash
docker compose -f docker-compose.prod.yml up --build
```

Якщо `ENVIRONMENT=production`, застосунок не стартує з дефолтним `SECRET_KEY` або дефолтним `ADMIN_PASSWORD`.

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

## Render

Для фронтенду в репозиторії є готовий [render.yaml](C:/Users/acer3/PycharmProjects/praktychni_3j_kurs/render.yaml) під `Static Site`.

У ньому вже виставлено:

```env
VITE_API_URL=https://threej-kurs.onrender.com
```

і додано rewrite `/* -> /index.html`, щоб React Router коректно працював на прямих переходах на `/catalog`, `/booking`, `/admin` та інші маршрути.

Для backend на Render тепер підтримується звичайний `DATABASE_URL=postgresql://...` або `postgresql+psycopg://...`: конфіг автоматично нормалізує його для async SQLAlchemy.

Monitoring-контейнери у Render можна піднімати окремо пізніше, але для поточного деплойменту вони не потрібні, тому `render.yaml` спрощено саме під фронтенд.

## Додаткові матеріали

У папці `docs/` знаходяться user flow, flow diagram та low-fi wireframes сторінок.

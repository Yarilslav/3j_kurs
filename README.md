# Tea House “Asahi” Web Application (茶屋朝日)

## Опис проєкту
Веб-додаток для чайного дому “Асахі”, який дозволяє:
- переглядати каталог товарів;
- оформлювати замовлення;
- бронювати місця.

Система також надає базові інструменти для керування товарами, замовленнями та бронюваннями.

---

## Архітектура
Проєкт побудований як клієнт-серверна система:
- Backend: FastAPI
- Database: PostgreSQL
- Frontend: React (low-fi прототип, Vite)
- Контейнеризація: Docker Compose

---
## Запуск проєкту

```bash
docker compose up --build
Доступ до сервісів
Backend
API: 
http://127.0.0.1:8000
Swagger (OpenAPI): 
http://127.0.0.1:8000/docs
Metrics: 
http://127.0.0.1:8000/metrics
Frontend
React frontend: 
http://127.0.0.1:5173
Monitoring
Prometheus: 
http://127.0.0.1:9090
Grafana: 
http://127.0.0.1:3000


## Основні API endpoint-и:
Auth
POST /register
POST /login
GET /me
Users
GET /users/
POST /users/
PUT /users/{user_id}
DELETE /users/{user_id}
PATCH /users/by-login/{login}/role
Products
GET /products/
GET /products/{id}
POST /products/
PUT /products/{id}
DELETE /products/{id}
Orders
POST /orders/
GET /orders/
PATCH /orders/{order_id}/status
Reservations
POST /reservations/
GET /reservations/
PATCH /reservations/{reservation_id}/status

## Приклади запитів:

Реєстрація користувача
POST /register
{
  "name": "Asahi Guest",
  "email": "guest@example.com",
  "login": "asahiguest",
  "phone_number": "+380501234567",
  "password": "123456"
}

Отримання списку товарів
GET /products/

Створення замовлення
POST /orders/
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "address": "Kyiv, Example street 1",
  "guest_name": "Asahi Guest",
  "guest_contact": "guest@example.com"
}

Створення бронювання
POST /reservations/
{
  "reservation_at": "2026-05-10 18:00",
  "places": [1, 2],
  "guest_name": "Asahi Guest",
  "guest_contact": "guest@example.com"
}


## Frontend

Frontend реалізовано як low-fi прототип на React + Vite.

Основні маршрути frontend
/ — головна сторінка;
/auth — сторінка входу та реєстрації;
/catalog — каталог товарів;
/catalog/:id — сторінка окремого товару;
/booking — сторінка бронювання;
/admin — демонстраційна admin-панель.
Призначення frontend
демонстрація структури інтерфейсу;
навігація між сторінками;
відображення основних користувацьких сценаріїв;
базова інтеграція з backend API.


## Додаткові матеріали
У папці docs/ знаходяться:
User Flow;
Flow Diagram;
low-fi Wireframes сторінок.


Технології
FastAPI
PostgreSQL
React
Vite
Docker / Docker Compose
Prometheus
Grafana
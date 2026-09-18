# Barber-API 💈

REST API for a barbershop appointment booking system, built with **Django** and **Django REST Framework**. It powers [Barber-Frontened](https://github.com/alejandro-cardenas-dev/Barber-Frontened) — handling authentication, barber schedules/availability, service catalog, and appointment booking for customers, barbers, and admins.

> 🔗 Frontend repo: [Barber-Frontened](https://github.com/alejandro-cardenas-dev/Barber-Frontened)
> 📄 API docs (Swagger/ReDoc): available at `/swagger/` and `/redoc/` once running

## Tech Stack

- **Framework:** Django 5.2 + Django REST Framework
- **Auth:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL (via `dj-database-url` / `psycopg2`)
- **Docs:** Auto-generated Swagger & ReDoc via `drf-yasg`
- **Static files:** WhiteNoise
- **CORS:** `django-cors-headers`
- **Server:** Gunicorn (production)
- **Deployment:** Render

## Data Model

- **User** — custom user model (email-based login). Every user has exactly one role: `is_customer`, `is_barber`, or `is_staff` (admin), enforced by a DB constraint.
- **Customer** — 1:1 profile linked to a `User` with `is_customer=True`.
- **Barber** — 1:1 profile linked to a `User` with `is_barber=True`. Stores working hours and lunch break, and generates available time slots from them.
- **Service** — a bookable service (name, description, price).
- **Appointment** — links a `Barber`, `Customer`, and `Service` on a date/time, with status (`confirmed`, `cancelled`, `completed`). A unique constraint prevents double-booking the same barber slot, and appointments auto-transition to `completed` once their time has passed.

## API Overview

All endpoints are prefixed with `/api/`.

| Endpoint | Description |
| --- | --- |
| `POST /api/token/` | Obtain JWT access + refresh tokens (login) |
| `POST /api/token/refresh/` | Refresh an access token |
| `POST /api/users/` | Create a new account (signup) |
| `GET /api/users/me/` | Get the authenticated user's profile |
| `GET /api/barbers/` | List barbers |
| `GET /api/barbers/<id>/` | Barber detail (admin) |
| `GET/PUT /api/barbers/me/schedule/` | View/update the logged-in barber's schedule |
| `GET /api/barbers/<id>/available-times/` | Available time slots for a barber on a given date |
| `GET/POST /api/services/` | List / create services |
| `GET/PUT/DELETE /api/services/<id>/` | Retrieve, update, or delete a service |
| `GET/POST /api/appointments/` | List / create appointments |
| `POST /api/appointments/<id>/cancel/` | Cancel an appointment |
| `DELETE /api/appointments/<id>/` | Delete an appointment |

For full request/response schemas, run the project and check `/swagger/`.

## Project Structure

The project is organized by Django app, with each domain app following a consistent internal layout (serializers, services, views split out rather than a single `views.py`/`serializers.py`):

```
barbershop_api/       # Project settings, root URLs, WSGI/ASGI
apps/
├── users/            # Custom User model, auth-related endpoints
│   └── management/commands/create_admin.py   # Creates a superuser on deploy
├── customers/         # Customer profile
├── barbers/            # Barber profile, schedules, availability
├── catalog/             # Services
└── appointments/         # Appointment booking, cancellation, status logic

each app/
├── models.py
├── serializers/
├── services/          # Business logic, kept out of views
├── views/
├── urls.py
└── admin.py
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (or adjust `DATABASE_URL` for another engine dj-database-url supports)

### 1. Clone the repo

```bash
git clone https://github.com/alejandro-cardenas-dev/Barber-API.git
cd Barber-API
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/barbershop
ADMIN_EMAIL=admin@barbershop.com
ADMIN_PASSWORD=change-me
```

`DEBUG` is automatically `True` unless the `RENDER` environment variable is set (i.e. it's `True` locally, `False` in production on Render).

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`, with docs at `http://localhost:8000/swagger/`.

## Authentication

Auth uses JWT via `djangorestframework-simplejwt`:

1. `POST /api/token/` with `email` and `password` → returns `access` and `refresh` tokens
2. Send the access token on subsequent requests: `Authorization: Bearer <access_token>`
3. Access tokens expire after 20 minutes; use `POST /api/token/refresh/` with the refresh token (valid 7 days, rotated on each use) to get a new one

## CORS

Allowed origins are configured in `barbershop_api/settings.py` (`CORS_ALLOWED_ORIGINS`) and currently include `http://localhost:3000` and the deployed frontend URL. Update this list if you deploy the frontend elsewhere.

## Deployment

The included `build.sh` is set up for [Render](https://render.com):

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin
```

`create_admin` is a custom management command that provisions/updates a staff admin user on every deploy, using the `ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables (defaults to `admin@barbershop.com` / `temporal123` if unset — **override these in production**).
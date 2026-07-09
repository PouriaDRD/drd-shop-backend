# DRD Shop Backend

DRD Shop Backend is a Django REST Framework based backend designed with a scalable architecture and clean separation of responsibilities.

The project follows a layered architecture consisting of:

* Models
* Repositories
* Services (Business Layer)
* Selectors
* Serializers
* API Views
* Celery Tasks

It includes authentication, OTP login, notifications, wallet, finance, shop, support ticket system, referral system, coupon system and many other modules.

---

# Requirements

* Python 3.13+
* PostgreSQL
* Redis
* Celery
* Git

---

# Installation

## Clone the project

```bash
git clone "https://github.com/PouriaDRD/drd-shop-backend.git"

cd drd-shop-backend
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment File

Create a `.env` file in the project root.

Example:

```env
STAGE="development"
DEBUG="True"
...
```

All available environment variables are explained below.

---

## Run Database Migrations

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

---

## Run Celery Worker

```bash
celery -A config worker -l info
```

---

## Run Celery Beat (Optional)

```bash
celery -A config beat -l info
```

---

# Project Architecture

```
apps/
│
├── accounts/
├── authentication/
├── finance/
├── notifications/
├── commerce/
├── support/
├── config/
├── billing/
│
└── shared/
```

Each app follows a similar architecture:

```
app/
│
├── admin/
├── api/
├── enums/
├── exceptions/
├── models/
├── repositories/
├── selectors/
├── serializers/
├── services/
├── tasks/
├── tests/
└── urls.py
```

---

# Environment Variables

---

## Application

### STAGE

Application environment.

Possible values:

```
development
production
testing
```

Example

```env
STAGE="development"
```

---

### DEBUG

Enables Django debug mode.

Development

```env
DEBUG="True"
```

Production

```env
DEBUG="False"
```

---

### BASE_URL

Base URL prefix for REST APIs.

Example

```env
BASE_URL="api/"
```

API Example

```
/api/auth/login/
/api/commerce/products/
```

---

### ADMIN_URL

Admin panel URL.

Example

```env
ADMIN_URL="admin/"
```

Admin Panel

```
/admin/
```

---

### SECRET_KEY

Django secret key used for cryptographic signing.

Never expose this key publicly.

Example

```env
SECRET_KEY="your-secret-key"
```

---

# Internationalization

### LANGUAGE_CODE

Default application language.

Example

```env
LANGUAGE_CODE="en-us"
```

---

### TIME_ZONE

Application timezone.

Example

```env
TIME_ZONE="Asia/Tehran"
```

---

### USE_I18N

Enable translation system.

```
True
False
```

---

### USE_TZ

Enable timezone-aware datetimes.

Recommended

```env
USE_TZ="True"
```

---

# Email Configuration

These settings configure the SMTP server used to send emails.

Used for:

* OTP emails
* Login notifications
* Registration notifications
* Password reset
* System notifications

---

### EMAIL_BACKEND

Email backend implementation.

Example

```env
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
```

---

### EMAIL_HOST

SMTP server hostname.

Example

```env
EMAIL_HOST="smtp.gmail.com"
```

---

### EMAIL_PORT

SMTP port.

Common values

```
587
465
```

---

### EMAIL_USE_TLS

Enable TLS encryption.

```
True
False
```

---

### EMAIL_USE_SSL

Enable SSL encryption.

```
True
False
```

---

### EMAIL_HOST_USER

SMTP username.

Usually your email address.

---

### EMAIL_HOST_PASSWORD

SMTP password or App Password.

Never commit this value to Git.

---

### DEFAULT_FROM_EMAIL

Default sender email.

Example

```env
DEFAULT_FROM_EMAIL="noreply@example.com"
```

---

### MAX_RETRY_ATTEMPTS

Maximum retry count when sending emails fails.

Example

```env
MAX_RETRY_ATTEMPTS="3"
```

---

# Celery Configuration

Used for asynchronous background jobs.

Examples:

* Email sending
* Notifications
* Scheduled jobs

---

### CELERY_BROKER_URL

Redis broker URL.

Example

```env
CELERY_BROKER_URL="redis://localhost:6379/0"
```

---

### CELERY_RESULT_BACKEND

Stores Celery task results.

Usually Redis.

```env
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

---

# Authentication Configuration

---

### OTP_LENGTH

Length of generated OTP codes.

Example

```env
OTP_LENGTH="6"
```

---

### OTP_TTL_MINUTES

OTP expiration time.

Example

```env
OTP_TTL_MINUTES="2"
```

---

### MAX_OTP_ATTEMPTS

Maximum invalid OTP attempts.

Example

```env
MAX_OTP_ATTEMPTS="3"
```

---

### ACCESS_TOKEN_LIFETIME

JWT Access Token lifetime in days.

Example

```env
ACCESS_TOKEN_LIFETIME="1"
```

---

### REFRESH_TOKEN_LIFETIME

JWT Refresh Token lifetime in days.

Example

```env
REFRESH_TOKEN_LIFETIME="7"
```

---

# Networking & Security

---

## INTERNAL_IPS

Trusted internal IP addresses.

Used by:

* Django Debug Toolbar
* Internal development middleware

Example

```env
INTERNAL_IPS="localhost,127.0.0.1"
```

---

## ALLOWED_HOSTS

Allowed hostnames for Django.

Security critical.

Development

```env
ALLOWED_HOSTS="localhost,127.0.0.1"
```

Production

```env
ALLOWED_HOSTS="api.example.com"
```

---

## CORS_ALLOW_CREDENTIALS

Allow cookies and Authorization headers across origins.

Usually

```env
True
```

---

## CORS_ALLOWED_ORIGINS

Frontend applications allowed to access the API.

Example

```env
CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

---

## CSRF_TRUSTED_ORIGINS

Trusted origins for CSRF validation.

Required when using:

* Django Admin
* Session Authentication
* Cookies

Example

```env
CSRF_TRUSTED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

---

# Useful Commands

Run server

```bash
python manage.py runserver
```

Run migrations

```bash
python manage.py migrate
```

Create migrations

```bash
python manage.py makemigrations
```

Create superuser

```bash
python manage.py createsuperuser
```

Run Celery Worker

```bash
celery -A config worker -l info
```

Run Celery Beat

```bash
celery -A config beat -l info
```

Collect static files

```bash
python manage.py collectstatic
```

Run tests

```bash
python manage.py test
```

---

# Features

* JWT Authentication
* Email OTP Authentication
* Login History
* Notification System
* Wallet
* Finance Module
* Shop System
* Product Plans
* Coupon System
* Referral System
* Support Ticket System
* File Attachments
* Celery Background Tasks
* Email Templates
* Clean Architecture
* Repository Pattern
* Service Layer
* Selector Layer
* Django Admin Panel
* REST API
* PostgreSQL Support
* Redis Support

---

# License

This project is developed for **DRD Shop**.

All rights reserved.

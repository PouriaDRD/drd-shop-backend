from .base import *

DEBUG = True
ENABLE_DEBUG_TOOLBAR = True

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "dev_db.sqlite3",
    }
}

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# ---------------------------------------------------------------
# Allowed Hosts & Internal IPs
# ---------------------------------------------------------------
INTERNAL_IPS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ---------------------------------------------------------------
# CORS & CSRF Configuration
# ---------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


# ---------------------------------------------------------------
# Static & Media Files
# ---------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

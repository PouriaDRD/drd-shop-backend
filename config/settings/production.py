from .base import *

DEBUG = False
ENABLE_DEBUG_TOOLBAR = False

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "prod_db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB"),
#         "USER": os.getenv("POSTGRES_USER"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
#         "HOST": os.getenv("POSTGRES_HOST"),
#         "PORT": os.getenv("POSTGRES_PORT", "5432"),
#     }
# }


# ---------------------------------------------------------------
# Allowed Hosts & Internal IPs
# ---------------------------------------------------------------
INTERNAL_IPS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = [
    "example.com",
    "www.example.com",
    "sub.example.com",
]

# ---------------------------------------------------------------
# CORS & CSRF Configuration
# ---------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://example.com",
    "https://api.example.com",
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


# ---------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "[{asctime}] "
                "[{levelname}] "
                "[{name}] "
                "{module}:{lineno} "
                "{message}"
            ),
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "django_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
            "level": "ERROR",
        },
        "security_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "security.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
        },
        "api_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "api.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": [
            "console",
            "django_file",
            "error_file",
        ],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
                "django_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": [
                "error_file",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": [
                "security_file",
            ],
            "level": "WARNING",
            "propagate": False,
        },
        "api": {
            "handlers": [
                "api_file",
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}

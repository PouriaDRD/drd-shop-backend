import os
from pathlib import Path
from datetime import timedelta

from config.settings.app_config import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config.app.secret_key


AUTH_USER_MODEL = "accounts.UserModel"


# ---------------------------------------------------------------
# Installed Apps Configuration
# ---------------------------------------------------------------
INSTALLED_APPS = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "corsheaders",
    "django_filters",
    "rest_framework",
    "django_cleanup.apps.CleanupSelectedConfig",
    # Custom apps
    "accounts",
    "authentication",
    "finance",
]

# ---------------------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------
# URL Configuration
# ---------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------
LANGUAGE_CODE = config.i18n.language_code

TIME_ZONE = config.i18n.time_zone

USE_I18N = config.i18n.use_i18n

USE_TZ = config.i18n.use_tz


# ---------------------------------------------------------------
# Django REST Framework Configuration
# ---------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/minute",
        "user": "40/minute",
        "refresh-token": "5/minute",
        "request-otp": "2/minute",
        "verify-otp": "5/minute",
    },
    "EXCEPTION_HANDLER": "config.utils.exceptions.custom_exception_handler",
}

# ---------------------------------------------------------------
# Email Configuration
# ---------------------------------------------------------------
EMAIL_BACKEND = config.email.backend
EMAIL_HOST = config.email.host
EMAIL_PORT = config.email.port
EMAIL_USE_TLS = config.email.use_tls
EMAIL_HOST_USER = config.email.host_user
EMAIL_HOST_PASSWORD = config.email.host_password
DEFAULT_FROM_EMAIL = config.email.default_from_email

# ---------------------------------------------------------------
# Simple JWT Configuration
# ---------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=config.auth.access_token_lifetime),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config.auth.refresh_token_lifetime),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": True,
}


# ---------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # -----------------------------------------------------------
    # Formatters
    # -----------------------------------------------------------
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
    # -----------------------------------------------------------
    # Handlers
    # -----------------------------------------------------------
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "django_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "when": "midnight",
            "backupCount": 60,
            "formatter": "verbose",
            "level": "ERROR",
        },
        "security_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "security.log",
            "when": "midnight",
            "backupCount": 60,
            "formatter": "verbose",
            "level": "WARNING",
        },
        "accounts_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "accounts.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
        "authentication_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "authentication.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
        "finance_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "finance.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
    },
    # -----------------------------------------------------------
    # Root Logger
    # -----------------------------------------------------------
    "root": {
        "handlers": [
            "console",
            "error_file",
        ],
        "level": "INFO",
    },
    # -----------------------------------------------------------
    # Loggers
    # -----------------------------------------------------------
    "loggers": {
        "django": {
            "handlers": [
                "django_file",
                "console",
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
        "accounts": {
            "handlers": [
                "accounts_file",
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "authentication": {
            "handlers": [
                "authentication_file",
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "finance": {
            "handlers": [
                "finance_file",
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}

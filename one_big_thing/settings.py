from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_base import (
    BASE_DIR,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    STATICFILES_STORAGE,
    env,
)

STATIC_URL = STATIC_URL
STATICFILES_DIRS = STATICFILES_DIRS
STATIC_ROOT = STATIC_ROOT
STATICFILES_STORAGE = STATICFILES_STORAGE

ENVIRONMENT = env.str("ENVIRONMENT", default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

REQUIRED_LEARNING_TIME = env.int("REQUIRED_LEARNING_TIME", default=420)

VCAP_APPLICATION = env.json("VCAP_APPLICATION", default={})
CONTACT_EMAIL = env.str("CONTACT_EMAIL", default="test@example.com")
FROM_EMAIL = env.str("FROM_EMAIL", default="test@example.com")
FEEDBACK_EMAIL = env.str("FEEDBACK_EMAIL", default="test@example.com")
ALLOWED_DOMAINS = env.str("ALLOWED_DOMAINS", default="").split(",")

CIVIL_SERVICE_DOMAINS = frozenset(ALLOWED_DOMAINS)

BASIC_AUTH = env.str("BASIC_AUTH", default="")

BASE_URL = env.str("BASE_URL")

APPEND_SLASH = True

ALLOWED_CIDR_NETS = ["10.0.0.0/16"]

ALLOWED_HOSTS = [
    "obt-server",
    "one-big-thing-develop.london.cloudapps.digital",
    "localhost",
    "127.0.0.1",
    "dev.onebigthing.civilservice.gov.uk",
    "onebigthing.civilservice.gov.uk",
    "web",
    "testserver",
]

# CSRF settings
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [
    "dev.onebigthing.civilservice.gov.uk",
    "onebigthing.civilservice.gov.uk",
]

if VCAP_APPLICATION.get("space_name", "unknown") not in ["tests", "local"]:
    SESSION_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    "one_big_thing.learning",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "single_session",
    "rest_framework",
    "django_otp",
    "django_otp.plugins.otp_totp",
]

CORS_APPS = [
    "corsheaders",
]

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + CORS_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

CORS_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

if DEBUG:
    MIDDLEWARE = MIDDLEWARE + CORS_MIDDLEWARE

if not DEBUG:
    SECURE_HSTS_SECONDS = 2 * 365 * 24 * 60 * 60  # Mozilla guidance max-age 2 years
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True


if BASIC_AUTH:
    MIDDLEWARE = ["one_big_thing.auth.basic_auth_middleware"] + MIDDLEWARE

ROOT_URLCONF = "one_big_thing.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            BASE_DIR / "one_big_thing" / "templates",
        ],
        "OPTIONS": {"environment": "one_big_thing.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "one_big_thing" / "templates" / "allauth",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "one_big_thing.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
        **{"ATOMIC_REQUESTS": True},
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "one_big_thing.custom_password_validators.SpecialCharacterValidator",
    },
    {
        "NAME": "one_big_thing.custom_password_validators.LowercaseUppercaseValidator",
    },
    {
        "NAME": "one_big_thing.custom_password_validators.BusinessPhraseSimilarityValidator",
    },
]

if not DEBUG:
    SENTRY_DSN = env.str("SENTRY_DSN", default="")
    SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", default="")

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],
        environment=SENTRY_ENVIRONMENT,
        send_default_pii=False,
        traces_sample_rate=1.0,
        profiles_sample_rate=0.0,
    )

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "learning.User"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "homepage"
LOGIN_URL = "index"

ALLOW_EXAMPLE_EMAILS = env.bool("ALLOW_EXAMPLE_EMAILS", default=True)

if ALLOW_EXAMPLE_EMAILS:
    ALLOWED_CIVIL_SERVICE_DOMAINS = CIVIL_SERVICE_DOMAINS.union({"example.com"})
    # This is domain is used for testing, so for these purposes, count it as a CS domain
else:
    ALLOWED_CIVIL_SERVICE_DOMAINS = CIVIL_SERVICE_DOMAINS

PASSWORD_RESET_TIMEOUT = 60 * 60

# Email

EMAIL_BACKEND_TYPE = env.str("EMAIL_BACKEND_TYPE")

if EMAIL_BACKEND_TYPE == "FILE":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = env.str("EMAIL_FILE_PATH")
elif EMAIL_BACKEND_TYPE == "CONSOLE":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_BACKEND_TYPE == "GOVUKNOTIFY":
    EMAIL_BACKEND = "django_gov_notify.backends.NotifyEmailBackend"
    GOVUK_NOTIFY_API_KEY = env.str("GOVUK_NOTIFY_API_KEY")
    GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID = env.str("GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID")
else:
    if EMAIL_BACKEND_TYPE not in ("FILE", "CONSOLE", "GOVUKNOTIFY"):
        raise Exception(f"Unknown EMAIL_BACKEND_TYPE of {EMAIL_BACKEND_TYPE}")

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 60 * 60 * 24 * 120  # 120 days
    SESSION_COOKIE_SAMESITE = "Strict"


PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "fullscreen": [],
    "gamepad": [],
    "geolocation": [],
    "gyroscope": [],
    "microphone": [],
    "midi": [],
    "payment": [],
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"


CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'sha256-wQJppp72tbAs/gAyLSJEgQfdtams9qseMear9achv1o='")

OTP_TOTP_ISSUER = "OneBigThing"
OTP_TOTP_AUTOCONF = True
OTP_TOTP_KEY_LENGTH = 16
OTP_TOTP_THROTTLE_FACTOR = 1.0

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

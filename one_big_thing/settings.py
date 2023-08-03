import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .db import fetch_db_password, get_secret
from .settings_base import (
    BASE_DIR,
    SECRET_KEY,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    env,
)

SECRET_KEY = SECRET_KEY
STATIC_URL = STATIC_URL
STATICFILES_DIRS = STATICFILES_DIRS
STATIC_ROOT = STATIC_ROOT

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ENVIRONMENT = env.str("ENVIRONMENT", default=None)

REQUIRED_LEARNING_TIME = env.int("REQUIRED_LEARNING_TIME", default=420)
SELF_REFLECTION_FILENAME = env.str("SELF_REFLECTION_FILENAME")

CONTACT_EMAIL = env.str("CONTACT_EMAIL", default="test@example.com")
FROM_EMAIL = env.str("FROM_EMAIL", default="test@example.com")
FEEDBACK_EMAIL = env.str("FEEDBACK_EMAIL", default="test@example.com")
VCAP_APPLICATION = env.json("VCAP_APPLICATION", default={})
if not ENVIRONMENT:
    ALLOWED_DOMAINS = env.list("ALLOWED_DOMAINS", default=list())
else:
    ALLOWED_DOMAINS = get_secret("ALLOWED_DOMAINS")

CIVIL_SERVICE_DOMAINS = frozenset(ALLOWED_DOMAINS)

BASIC_AUTH = env.str("BASIC_AUTH", default="")

BASE_URL = env.str("BASE_URL")

DEPARTMENTS_USING_INTRANET = dict(env.json("DEPARTMENTS_USING_INTRANET", default={}))

APPEND_SLASH = True

ALLOWED_CIDR_NETS = ["10.0.0.0/16"]

ALLOWED_HOSTS = [
    "one-big-thing-testserver",
    "one-big-thing-develop.london.cloudapps.digital",
    "localhost",
    "127.0.0.1",
    "obt-dev.i.ai.10ds.cabinetoffice.gov.uk",
]

# CSRF settings
CSRF_COOKIE_HTTPONLY = True

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
]

CORS_APPS = [
    "corsheaders",
]

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + CORS_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allow_cidr.middleware.AllowCIDRMiddleware",
]

CORS_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

if DEBUG:
    MIDDLEWARE = MIDDLEWARE + CORS_MIDDLEWARE

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
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD")
        if not ENVIRONMENT
        else fetch_db_password(env.str("DB_PASSWORD_SECRET_NAME")),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
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
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SENTRY_DSN = env.str("SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", default="")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
    ],
    environment=SENTRY_ENVIRONMENT,
    send_default_pii=False,
    traces_sample_rate=0.0,
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
LOGIN_URL = "account_signup"

ALLOW_EXAMPLE_EMAILS = env.bool("ALLOW_EXAMPLE_EMAILS", default=True)

if ALLOW_EXAMPLE_EMAILS:
    ALLOWED_CIVIL_SERVICE_DOMAINS = CIVIL_SERVICE_DOMAINS.union({"example.com"})
    # This is domain is used for testing, so for these purposes, count it as a CS domain
else:
    ALLOWED_CIVIL_SERVICE_DOMAINS = CIVIL_SERVICE_DOMAINS

SEND_VERIFICATION_EMAIL = env.bool("SEND_VERIFICATION_EMAIL", default=False)

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24

# Email

EMAIL_BACKEND_TYPE = env.str("EMAIL_BACKEND_TYPE")

if EMAIL_BACKEND_TYPE == "FILE":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = env.str("EMAIL_FILE_PATH")
elif EMAIL_BACKEND_TYPE == "CONSOLE":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_BACKEND_TYPE == "GOVUKNOTIFY":
    EMAIL_BACKEND = "django_gov_notify.backends.NotifyEmailBackend"
    if not ENVIRONMENT:
        GOVUK_NOTIFY_API_KEY = env.str("GOVUK_NOTIFY_API_KEY")
        GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID = env.str("GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID")
    else:
        GOVUK_NOTIFY_API_KEY = get_secret("GOVUK_NOTIFY_API_KEY")
        GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID = get_secret("GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID")
else:
    if EMAIL_BACKEND_TYPE not in ("FILE", "CONSOLE", "GOVUKNOTIFY"):
        raise Exception(f"Unknown EMAIL_BACKEND_TYPE of {EMAIL_BACKEND_TYPE}")

SEND_VERIFICATION_EMAIL = env.bool("SEND_VERIFICATION_EMAIL", default=False)

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 60 * 60 * 24 * 120  # 120 days
    SESSION_COOKIE_SAMESITE = "Strict"

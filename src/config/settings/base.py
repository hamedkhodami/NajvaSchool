import os
from pathlib import Path

from dotenv import load_dotenv


# -----------------------------------------------------------------


# ---BASE_DIR------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# -----------------------------------------------------------------


# ---ENV-----------------------------------------------------------
load_dotenv(dotenv_path=BASE_DIR / ".env")
# -----------------------------------------------------------------


# ---SECURITY------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = bool(int(os.getenv("DEBUG")))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
# -----------------------------------------------------------------


# ---CSRF---------------------------------------------------------
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED",
).split(",")
# ----------------------------------------------------------------


# ---Application definition---------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "apps.core.apps.CoreConfig",
    "apps.account.apps.AccountConfig",
    "apps.student.apps.StudentConfig",
    "apps.teacher.apps.TeacherConfig",
    "apps.academic.apps.AcademicConfig",
    "apps.attendance.apps.AttendanceConfig",
    "apps.education.apps.EducationConfig",
    "apps.finance.apps.FinanceConfig",
    "apps.payment.apps.PaymentConfig",
    "apps.notification.apps.NotificationConfig",
    "apps.public.apps.PublicConfig",
    "apps.dashboard.apps.DashboardConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
# ----------------------------------------------------------------


# ---TEMPLATES----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
# ----------------------------------------------------------------


# ---WSGI---------------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"
# ----------------------------------------------------------------


# ---Auth Password Validators---------------------------------------------------------
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
# ----------------------------------------------------------------


# ---Internationalization------------------------------------------
LANGUAGES = [
    ("fa", "Persian"),
]

LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True
# ----------------------------------------------------------------


# ---Static files-------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / os.getenv("STATIC_ROOT", "staticfiles")
# ----------------------------------------------------------------


# ---Media--------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / os.getenv("MEDIA_ROOT", "static/media")
# ----------------------------------------------------------------


# ---Default primary key field type------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ---------------------------------------------------------------


# ---Auth-------------------------------------------------------
AUTH_USER_MODEL = "account.User"
# ---------------------------------------------------------------


# ---Redis-------------------------------------------------------
REDIS_CONFIG = {
    "DB": int(os.getenv("REDIS_DB", 0)),
    "HOST": os.getenv("REDIS_HOST", "redis"),
    "PORT": int(os.getenv("REDIS_PORT", 6379)),
    "CHANNEL_NAME": os.getenv("REDIS_CHANNEL_NAME", "market_price"),
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# ---------------------------------------------------------------


# ---SMS config -------------------------------------------------
SMS_CONFIG = {
    "API_KEY": os.getenv("SMS_CONFIG_API_KEY"),
    "ORIGINATOR": os.getenv("SMS_CONFIG_ORIGINATOR"),
}
# ---------------------------------------------------------------

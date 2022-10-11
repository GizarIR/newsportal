"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os.path
from pathlib import Path

# TODO: Безопасное хранение паролей (реализован), но есть способ проще  - надо проверить
# есть более простой способ который нужно проверить:
# 1. создаем файл .env там же где manage.py и  добавляем в него  PASSWORD=fhgjhs или любые переменные
# 2. добавляем его в .gitignore
# 3. import os
# 4. в settings.py PSWD=os.getenv("PASSWORD") , константа становиться доступной для использования
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
PASSWORD_EMAIL = os.environ.get("PASSWORD_EMAIL")
EMAIL_ADMIN = os.environ.get("EMAIL_ADMIN")
ADMIN_EMAIL_SERVER = os.environ.get("ADMIN_EMAIL_SERVER")

MY_EMAIL_HOST = os.environ.get("MY_EMAIL_HOST")
MY_EMAIL_HOST_USER = os.environ.get("MY_EMAIL_HOST_USER")


# импорт переводов
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gk4-vyka9h-yqh(5w7@r!=u_uuc%-n5_+cae4!!c5=3=pe9w1p'



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation', # обязательно вписываем его перед админом

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #добавленные приложения
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    # 'news',
    'django_filters',
    # расширим название приложения в связи с настройкой работы сигналов
    'news.apps.NewsConfig',
    # добавим приложения для рагистрации и аторизации
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable for work allauth library:
    'allauth.socialaccount.providers.google',
#    модуль за запуска задач по расписанию
    'django_apscheduler',
    'rest_framework',
    'restapp',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware', # добавлен для включения функции перевода, порядок важен

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # подключаем еще один middle
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # подключаем созданный по инструкции мидлваре для локализации времени
    'news.middlewares.TimezoneMiddleware',

]

ROOT_URLCONF = 'NewsPortal.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # добавим путь при до шаблонов - делаем это при настройке flatpages и др. приложений
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'news/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # для работы allauth
                'django.template.context_processors.request',
                # для переменных который нужны во многих шаблонах
                'news.context_processors.extra_context',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru' # переключено на русский язык при внедрении перевода

LANGUAGES = [
    ('en-us' , 'English'),
    ('ru','Русский'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
# MODELTRANSLATION_LANGUAGES = ('en-us', 'ru')
# MODELTRANSLATION_FALLBACK_LANGUAGES = ('ru',)


# TIME_ZONE = 'Europe/Moscow' #по умолчанию было UTC

TIME_ZONE = 'UTC' #по умолчанию было UTC


USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR/"static"
]


# далее идут  переменные добавленные в ходе разработки приложения

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home_news'
LOGOUT_REDIRECT_URL  = 'home_news'

DEFAULT_FROM_EMAIL = EMAIL_ADMIN  # здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма

#добавляем константу
SITE_ID = 1

# Настройка аутентификации при помощи библиотеки allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none' - первоначальное значение до настройки почтовых уведомлений
# Строчка добавлена для того чтобы allauth библиотека знала что необходимо использовать видоизмененную
# форму регистрации пользователя SignupForm
ACCOUNT_FORMS = {'signup': 'news.forms.CommonSignupForm'}


# настройки почты
EMAIL_HOST = MY_EMAIL_HOST  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
# ниже ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами,
# это всё то что идёт до собаки
EMAIL_HOST_USER = MY_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = PASSWORD_EMAIL  # пароль от почты
# ниже Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках,
# но включать его здесь обязательно
EMAIL_USE_SSL = True

# для отправки критичных логов
ADMINS = [
    ('Gizar', EMAIL_ADMIN),
    # список всех админов в формате ('имя', 'их почта')
]
SERVER_EMAIL = ADMIN_EMAIL_SERVER

# (вариант - 2) Настройки задач по расписанию  - pip install django-apscheduler
# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше,
# но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# Группа настроек Redis для работы с Celery
# указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_BROKER_URL = 'redis://localhost:6379'
# указывает на хранилище результатов выполнения задач
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# допустимый формат данных.
CELERY_ACCEPT_CONTENT = ['application/json']
# метод сериализации задач
CELERY_TASK_SERIALIZER = 'json'
# метод сериализации результатов
CELERY_RESULT_SERIALIZER = 'json'

# Группа настроек кэширования
# Документация тут: https://django.fun/docs/django/ru/4.0/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # включаем кэширование на файлах
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы!
        # Не забываем создать папку cache_files внутри папки с manage.py!
        # 'TIMEOUT': 60, - можно устанавливать значение  сколько объект будет храниться в кэше (по умолчанию 300 сек)
    }
}


REST_FRAMEWORK = {
   'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
   'PAGE_SIZE': 5,
    # настройка что для доступа ко всем ViewSet ам требует аутентификация
    #     # ВАЖНО: permission_classes переопределяет стандартное значение в DEFAULT_PERMISSION_CLASSES, а значит,
    #     # если мы хотим отменить, то достаточно переопределить как permission_classes=[permissions.AllowAny]
    #     # или вообще permission_classes=[]
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False, # отключать ли предустановленные настройки логирования Джанго
#     'formatters': {
#         # INFO format
#         'i_format': {
#             'style': '{',
#             'format': '{asctime} | {levelname} | {module} | {message}',
#         },
#         # debug format
#         'd_format': {
#             'style': '{',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'format': '{asctime} | {levelname} | {message}',
#         },
#         # warning format
#         'w_format': {
#             'style': '{',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'format': '{asctime} | {levelname} | {pathname} | {message}',
#         },
#         # error and critical format
#         'e_c_format': {
#             'style': '{',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'format': '{asctime} | {levelname} | {pathname} | {exc_info} |{message}',
#         },
#         'mail_format': {
#             'style': '{',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'format': '{asctime} | {levelname} | {pathname} | {message}',
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'  # обрабатываем только когда параметр DEBUG = False в settings.py
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue' # обрабатываем только когда параметр DEBUG = True
#         },
#     },
#     'handlers':{
#         'console_i': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'i_format',
#         },
#         'console_d': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'd_format',
#         },
#         'console_w': {
#             'level': 'WARNING',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'w_format',
#         },
#         'console_e_c': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'e_c_format',
#         },
#         'general_log': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'logs/general.log',
#             'formatter': 'i_format',
#         },
#         'error_log': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.FileHandler',
#             'filename': 'logs/errors.log',
#             'formatter': 'e_c_format',
#         },
#         'security_log': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.FileHandler',
#             'filename': 'logs/security.log',
#             'formatter': 'i_format',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#             'formatter': 'mail_format',
#         },
#     },
#     'loggers':{
#         'django': {
#             'handlers': ['console_i', 'general_log'],
#             'level': 'DEBUG',
#         },
#         'console_debug': {
#             'handlers': ['console_d'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'console_warning': {
#             'handlers': ['console_w'],
#             'level': 'WARNING',
#             'propagate': False,
#         },
#         'console_e_c': {
#             'handlers': ['console_e_c'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'file_general': {
#             'handlers': ['general_log'],
#             'level': 'INFO',
#         },
#         'django.request': {
#             'handlers': ['error_log', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['error_log', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['error_log'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db_backends': {
#             'handlers': ['error_log'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['security_log'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }
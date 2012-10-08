from config.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT / 'db/development.sqlite3',
    }
}

DEBUG = True

#django-registration settings for dev
ACCOUNT_ACTIVATION_DAYS = 7

#Email debug settings (python -m smtpd -n -c DebuggingServer localhost:1025)
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'eddiehedges@gmail.com'

#django-simple-captcha settings
CAPTCHA_LENGTH = 4

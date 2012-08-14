from config.settings import *

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#django-registration settings for prod
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1023
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'password'

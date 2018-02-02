from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dpamz@&wa*x#0exclk6k*d&nfb9$&4q4x_*+85!e=uoqezus)t'  # todo: re-generate this secret key in its own file

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_ROOT = SITE_ROOT/'media'
MEDIA_URL = '/media/'

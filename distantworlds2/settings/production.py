from .base import *

# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = 'dpamz@&wa*x#0exclk6k*d&nfb9$&4q4x_*+85!e=uoqezus)t'  # todo: re-generate this secret key in its own file


DEBUG = False

MEDIA_ROOT = str(SITE_ROOT/'media')
MEDIA_URL = '/media/'

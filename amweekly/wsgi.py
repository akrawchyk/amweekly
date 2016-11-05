import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "amweekly.settings")


public_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'public')

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
application.add_files(public_path, prefix='/')

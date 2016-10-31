from django.conf import settings


def pytest_configure():
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test-amweekly'
        }
    }

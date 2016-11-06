from amweekly.settings import *  # noqa


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-amweekly'
    }
}

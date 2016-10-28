from django.db.models.signals import post_save

from factory import fuzzy
from factory.django import DjangoModelFactory, mute_signals


class MetaURLFactory(DjangoModelFactory):
    class Meta:
        model = 'amweekly.shares.MetaURL'
        django_get_or_create = ('url',)

    user_name = fuzzy.Faker('profile', fields=['username'])
    title = fuzzy.Faker('sentence')
    description = fuzzy.Faker('paragraph')
    url = fuzzy.Faker('url')


@mute_signals(post_save)
class ShareFactory(DjangoModelFactory):
    class Meta:
        model = 'amweekly.shares.Share'
        django_get_or_create = ('url',)

    og_title = fuzzy.Faker('sentence')
    og_description = fuzzy.Faker('paragraph')
    og_id = fuzzy.FuzzyInteger(0, 100)
    og_type = fuzzy.FuzzyText(length=10)
    url = fuzzy.Faker('url')

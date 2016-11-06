from django.db.models.signals import post_save

from factory import fuzzy, Faker
from factory.django import DjangoModelFactory, mute_signals


class MetaURLFactory(DjangoModelFactory):
    class Meta:
        model = 'shares.MetaURL'
        django_get_or_create = ('og_id', )

    og_title = Faker('sentence')
    og_description = fuzzy.FuzzyText(length=141)
    og_id = fuzzy.FuzzyInteger(0, 100)
    og_type = fuzzy.FuzzyText(length=10)


@mute_signals(post_save)
class ShareFactory(DjangoModelFactory):
    class Meta:
        model = 'shares.Share'

    user_name = Faker('profile', fields='username')
    title = Faker('sentence')
    description = fuzzy.FuzzyText(length=141)
    url = Faker('url')

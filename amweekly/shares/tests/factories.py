from factory import fuzzy, Faker
from factory.django import DjangoModelFactory


class MetaURLFactory(DjangoModelFactory):
    class Meta:
        model = 'shares.MetaURL'
        django_get_or_create = ('og_id', )

    og_title = Faker('sentence')
    og_description = Faker('paragraph')
    og_id = fuzzy.FuzzyInteger(0, 100)
    og_type = fuzzy.FuzzyText(length=10)


class ShareFactory(DjangoModelFactory):
    class Meta:
        model = 'shares.Share'
        django_get_or_create = ('url', )

    user_name = Faker('profile', fields='username')
    title = Faker('sentence')
    description = Faker('paragraphs', nb=10)
    url = Faker('url')

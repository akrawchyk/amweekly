from django.db.models.signals import post_save
from django.dispatch import receiver

from amweekly.shares.models import Share
from amweekly.slack.models import SlashCommand


@receiver(post_save, sender=SlashCommand, dispatch_uid='amweekly_slash_command')  # noqa
def amweekly_slash_command(sender, instance, **kwargs):
    if instance.command == '/djangoamweekly':
        Share.objects.create(
            user_name=instance.user_name,
            url=instance.text)

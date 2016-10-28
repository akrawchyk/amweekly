from django.db import models
from django.utils import timezone


class MetaURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    og_title = models.CharField(blank=True, max_length=255)
    og_description = models.TextField(blank=True)
    og_id = models.CharField(blank=True, max_length=255)
    og_type = models.CharField(blank=True, max_length=255)
    og_url = models.URLField()

    def __str__(self):
        if self.og_title != '':
            return self.og_title
        else:
            return self.og_url


class Share(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    meta_url = models.ForeignKey(
        'MetaURL',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    def __str__(self):
        return '{} on {}'.format(self.user_name, self.created_at)

    @property
    def get_title_display(self):
        if self.title:
            return self.title
        elif self.meta_url.og_title:
            return self.meta_url.og_title
        else:
            return self.url

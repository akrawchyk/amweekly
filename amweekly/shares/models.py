from django.db import models
from django.utils import timezone


class Share(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField()
    meta = models.ForeignKey('MetaURL', blank=True, null=True)
    user_name = models.CharField(max_length=255)

    def __str__(self):
        if self.meta is not None and self.meta.title is not None:
            return self.meta.title
        else:
            return self.url


class MetaURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField()
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(blank=True, max_length=255)

    def __str__(self):
        if self.title is not '':
            return self.title
        else:
            return self.url

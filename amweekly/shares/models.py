from django.db import models
from django.utils import timezone


class Share(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    meta = models.ForeignKey('MetaURL', blank=True, null=True)

    def __str__(self):
        return '{} on {}'.format(self.user_name, self.created_at)

    def save(self, *args, **kwargs):
        # ensure a meta_url is created before saving
        meta_url, created = MetaURL.objects.get_or_create(og_url=self.url)
        self.meta = meta_url
        super(Share, self).save(*args, **kwargs)


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

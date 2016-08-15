from django.db import models


class Share(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField()
    user_name = models.CharField(max_length=255)

    def __str__(self):
        return self.url

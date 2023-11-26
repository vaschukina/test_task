from django.db import models

class Site(models.Model):
    path = models.CharField(max_length=200)
    ip = models.CharField(max_length=200, null=True)
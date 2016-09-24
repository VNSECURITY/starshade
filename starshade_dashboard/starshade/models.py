import uuid

from django.db import models

class VirtualFix(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name="Name")
    patch = models.TextField(max_length=10000, blank=True, verbose_name="Script")

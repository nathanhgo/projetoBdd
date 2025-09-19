from django.db import models
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    description = models.CharField(max_length=255, null=True)

class Authors(models.Model):
    name = models.CharField(max_length=255, null=False)


class MetaBooks(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, null=False)
    pages = models.IntegerField()
    release_date = models.DateField(default=datetime.now, null=False)

class PhysicalBooks(models.Model):
    meta_book = models.ForeignKey(MetaBooks, on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=255, null=True)
    created_at = models.DateField(default=datetime.now, null=False)

class Transactions(models.Model):
    old_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, related_name='old_owner')
    new_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, related_name='new_owner')
    physical_book = models.ForeignKey(PhysicalBooks, on_delete=models.CASCADE, null=False)
    transaction_date = models.DateField(default=datetime.now, null=False)
    transaction_type = models.CharField(max_length=16, null=False)
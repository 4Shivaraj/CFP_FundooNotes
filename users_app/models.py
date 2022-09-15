from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.BigIntegerField()
    location = models.CharField(max_length=255)

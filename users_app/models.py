from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=255, unique=True)
    pass_word = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.BigIntegerField()
    location = models.TextField(max_length=255)

    def __str__(self):
        return self.user_name

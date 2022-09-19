from tkinter import CASCADE
from turtle import title
from django.db import models
from users_app.models import User


class Notes(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=1000)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class LastCheckedTender(models.Model):
    last_checked_tender = models.CharField(max_length=1000)
    tender = models.CharField(max_length=100)

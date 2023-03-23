from django.db import models
from django.contrib.auth import get_user_model


class Option(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    options = models.ManyToManyField(Option)

    def __str__(self) -> str:
        return self.user.get_username()

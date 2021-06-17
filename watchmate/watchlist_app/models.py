from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50)  # max_length does not work?
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

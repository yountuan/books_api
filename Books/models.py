from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.title} - {self.author}: {self.price} som'


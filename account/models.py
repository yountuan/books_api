from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserProfile(models.Model):
    city_choice = ((1, 'Bishkek'), (2, 'Osh'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.PositiveSmallIntegerField(choices=city_choice)
    address = models.CharField(max_length=300, blank=True)


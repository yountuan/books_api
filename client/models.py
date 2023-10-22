from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import JSONField
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    city_choice = ((1, 'Bishkek'), (2, 'Osh'))
    email = models.EmailField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    city = models.PositiveSmallIntegerField(choices=city_choice, default=1)
    address = models.TextField(blank=True)
    wishlist = JSONField(default=list)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        code = get_random_string(15)
        self.activation_code = code
        self.save()

    def send_activation_code(self, email, activation_code):
        message = f'''
        You are successfully registered in our web site. To activate your account please enter the code: {activation_code}
        '''

        send_mail(
            'Account activation',
            message,
            'test@gmail.com',
            [email]
        )
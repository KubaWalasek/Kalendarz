from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


class Adres(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True)
    post_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True )
    house_number = models.CharField(max_length=10, blank=True)
    apartment_number = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return f'{self.user.email} / {self.city}'
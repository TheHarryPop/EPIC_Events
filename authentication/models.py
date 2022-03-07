from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    MANAGEMENT = 'MANAGEMENT'
    SALES = 'SALES'
    SUPPORT = 'SUPPORT'

    ROLE_CHOICES = (
        (MANAGEMENT, 'Manager'),
        (SALES, 'Seller'),
        (SUPPORT, 'Support')
    )

    role = models.CharField(max_length=64, choices=ROLE_CHOICES, null=False, verbose_name='role')

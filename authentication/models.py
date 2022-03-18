from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    Management = 'Management'
    Sales = 'Sales'
    Support = 'Support'

    RoleChoices = (
        (Management, 'Manager'),
        (Sales, 'Seller'),
        (Support, 'Support')
    )

    role = models.CharField(max_length=64, choices=RoleChoices, null=False, verbose_name='role')

    def __str__(self):
        return f"User: {self.username} | Role: {self.role}"

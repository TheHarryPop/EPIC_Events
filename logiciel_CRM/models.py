from django.db import models
from django.conf import settings


class User(models.Model):

    class Role(models.TextChoices):
        MANAGEMENT = 'MANAGEMENT', 'MANAGEMENT'
        SALES = 'SALES', 'SALES'
        SUPPORT = 'SUPPORT', 'SUPPORT'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=True)
    username = models.CharField(max_length=64, null=False)
    password = models.CharField(max_length=64, null=False)
    role = models.CharField(max_length=64, choices=Role.choices, null=False)


class Customer(models.Model):
    sales_staff_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=64,unique=True, null=False)
    mobile = models.CharField(max_length=64,unique=True, null=False)
    company_name = models.CharField(max_length=64, null=False)
    date_created = models.DateField()
    date_updated = models.DateField()


class Contract(models.Model):
    sales_staff_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False)
    date_created = models.DateField()
    date_updated = models.DateField()
    amount = models.FloatField()
    status = models.BooleanField()
    payment_due = models.DateField()


class EventStatus(models.Model):
    status_description = models.CharField(max_length=64)


class Event(models.Model):
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False)
    support_staff_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    event_status_id = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE, null=False)
    event_date = models.DateField()
    date_created = models.DateField()
    date_updated = models.DateField()
    attendees = models.IntegerField()
    notes = models.CharField(max_length=2048)



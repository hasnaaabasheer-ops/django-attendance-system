from django.db import models
from django.utils import timezone


class Student(models.Model):

    name = models.CharField(
        max_length=150
    )

    roll_number = models.CharField(
        max_length=30,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    department = models.CharField(
        max_length=100
    )

    joining_date = models.DateField(
        default=timezone.localdate
    )

    photo = models.ImageField(
        upload_to='students/',
        blank=True
    )

    def __str__(self):
        return f'{self.roll_number} - {self.name}'
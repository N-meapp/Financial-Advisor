from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    age = models.IntegerField()
    job_position = models.CharField(max_length=30)

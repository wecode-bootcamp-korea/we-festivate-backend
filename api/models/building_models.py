from django.db import models

class buiding(models.Model):
    name = models.CharField(max_length=50, Unique=True)
    address = models.CharField(max_length=100)
    profile = models.CharField(max_length=500)
    contact = models.CharField(max_length=100)

from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    profile = models.CharField(max_length=500)
    contact = models.CharField(max_length=100)
    class Meta:
        db_table = "building"
        app_label= "event"

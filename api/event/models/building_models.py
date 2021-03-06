from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    profile = models.CharField(max_length=500)
    contact = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9,decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9,decimal_places=6, default=0)

    class Meta:
        db_table = "building"
#app_label= "event" (현재 버전에서는 필요 없다고 함)

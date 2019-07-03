from django.db import models
class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    profile = models.CharField(max_length=200)
    user_type = models.CharField(max_length=100, default="00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"


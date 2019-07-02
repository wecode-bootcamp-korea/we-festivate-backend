from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    user_pw = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100, unique=True)
    user_profile = models.CharField(max_length=200)
    user_type = models.CharField(max_length=100, default="00")
    member_building = models.CharField(max_length=100, default="0000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
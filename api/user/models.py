from django.db import models

class UserType(models.Model):
    type = models.CharField(max_length=30, default="non_wework_member")

    class Meta:
        db_table = "user_type"

class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    profile = models.CharField(max_length=200)
    user_type = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.CASCADE, default=1)
    # 1 : type = non_wework_member
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"


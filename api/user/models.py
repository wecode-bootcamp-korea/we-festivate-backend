from django.db import models

class UserType(models.Model):
    u_type = models.CharField(max_length=30, default="non_wework_member")

    class Meta:
        db_table = "user_type"

# class User(models.Model):
#     user_id    = models.CharField(max_length=20, unique=True)
#     password   = models.CharField(max_length=100)
#     name       = models.CharField(max_length=100)
#     email      = models.EmailField(max_length=100, unique=True)
#     profile    = models.CharField(max_length=200)
#     user_type  = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.CASCADE, default=1)
#     # 1 : type = non_wework_member
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = "user"

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"

#소셜로그인 수정
class User(models.Model):
    user_id         = models.CharField(max_length=100)
    password        = models.CharField(max_length=100)
    name            = models.CharField(max_length=100)
    email           = models.EmailField(max_length=100, unique=True, null=True)
    profile         = models.CharField(max_length=200)
    user_type       = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.CASCADE, default=1)
    # 1 : type      = non_wework_member
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"


from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)

class Friend(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    friend = models.ForeignKey(User, related_name="friends", default=0)
    created_at = models.DateTimeField(auto_now_add = True)

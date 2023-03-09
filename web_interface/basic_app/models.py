from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    age = models.IntegerField()
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length = 30)
    phone_number = models.IntegerField()
    #disorder_json = models.JSONField(default= {'available':0})
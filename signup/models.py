from django.db import models

# Create your models here.
# class UserDetails(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20)
#     password = models.CharField(max_length=100)
#     class Meta:
#         db_table='UserDetails'

class Userdetails(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=254)
    phone_number = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'userdetails'
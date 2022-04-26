from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class AddPortfolio(models.Model):
    date=models.DateField(null=False)
    objective=models.CharField(max_length=200)
    income=models.FloatField(null=True)
    expense=models.FloatField(null=True)
  

    class Meta:
        db_table="AddPortfolio"

class PersonalInfo(models.Model):
    first_name=models.CharField(max_length=200)
    middle_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    birth_data=models.DateTimeField()
    address=models.CharField(max_length=200)
    contact_number=models.DateTimeField()
    occupation=models.CharField(max_length=200)
    
    def __str__(self):
        return self.first_name

    class Meta:
        db_table="personal_info"

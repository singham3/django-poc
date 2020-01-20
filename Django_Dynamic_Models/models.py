from django.db import models
from adminapp.models import User
# Create your models here.


class DynamicModulesModel(models.Model):
    moduletitle = models.CharField(max_length=200)
    modulefiels = models.TextField(max_length=65500)
    moduledescription = models.TextField(max_length=5000)
    createat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)



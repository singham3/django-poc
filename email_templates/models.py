from django.db import models
from adminapp.models import User


class AddEmailHooksModel(models.Model):
    title = models.CharField(max_length=200,unique=True)
    hook = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    status = models.BooleanField(default=False)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)


class EmailTemplateModel(models.Model):
    emailhooks = models.ForeignKey(AddEmailHooksModel,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    ckeditor = models.TextField(max_length=65500)
    footer_text = models.CharField(max_length=200)
    email_preference = models.CharField(max_length=200)
    status = models.BooleanField(max_length=200,default=False)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)


class MainEmailLayoutModel(models.Model):
    title = models.CharField(max_length=200)
    layout_html = models.TextField(max_length=10000)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
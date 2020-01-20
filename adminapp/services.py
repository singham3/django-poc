from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from random import randint
from django.shortcuts import redirect


class CreateUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    mobile = forms.CharField()
    date = forms.CharField()
    email = forms.EmailField()
    userimg = forms.FileField()
    status = forms.CharField()
    password =forms.CharField()
    browser_type = forms.CharField()
    user_ip = forms.CharField()

    def process(self):
        dbsave = User(username=self.cleaned_data["username"], first_name=self.cleaned_data["first_name"], is_superuser=bool(int(self.cleaned_data["status"])),
                      is_staff=bool(self.cleaned_data["status"]), last_name=self.cleaned_data["last_name"], email=self.cleaned_data["email"],
                      is_active=bool(self.cleaned_data["status"]), mobile=self.cleaned_data["mobile"],
                      dateofbirth=datetime.strptime(self.cleaned_data["date"], '%m/%d/%Y'),
                      ismobile=False, isemail=False, userimg=self.cleaned_data["userimg"],
                      loginBrowser=self.cleaned_data["browser_type"], loginip=self.cleaned_data["user_ip"],
                      account_id=randint(10 ** (8 - 1), (10 ** 8) - 1))
        dbsave.set_password(self.cleaned_data["password"])
        dbsave.save()


class EditUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    mobile = forms.CharField()
    account_id = forms.CharField()
    date = forms.CharField()
    email = forms.EmailField()
    userimg = forms.FileField(required=False)
    password = forms.CharField(required=False)
    status = forms.CharField(required=False)
    browsertype = forms.CharField()
    userip = forms.CharField()

    def process(self):
        if User.objects.filter(account_id=int(self.cleaned_data['account_id']), username=self.cleaned_data['username'], email=self.cleaned_data['email']).exists():
            getuserdata = User.objects.get(account_id=int(self.cleaned_data['account_id']), username=self.cleaned_data['username'], email=self.cleaned_data['email'])
            if self.cleaned_data['first_name']:
                getuserdata.first_name = self.cleaned_data['first_name']
            if self.cleaned_data['last_name']:
                getuserdata.last_name = self.cleaned_data['last_name']
            getuserdata.mobile = self.cleaned_data['mobile']
            getuserdata.dateofbirth = datetime.strptime(self.cleaned_data["date"], '%m/%d/%Y')
            if self.cleaned_data['status']:
                getuserdata.is_active = bool(int(self.cleaned_data['status']))
                getuserdata.is_superuser = bool(int(self.cleaned_data['status']))
                getuserdata.is_staff = bool(int(self.cleaned_data['status']))
            getuserdata.loginBrowser = self.cleaned_data['browsertype']
            getuserdata.loginip = self.cleaned_data['userip']
            getuserdata.updatedat = datetime.now()
            if self.cleaned_data['userimg']:
                getuserdata.userimg = self.cleaned_data['userimg']
            if self.cleaned_data['password']:
                getuserdata.set_password(self.cleaned_data['password'])
            getuserdata.save()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher
User = get_user_model()
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from POC.admininfo import *

class Addadminform(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name =forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    date = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    userimg = forms.ImageField(required=True)
    status = forms.CharField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True,widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','first_name','last_name','mobile','date','userimg','status','password','confirm_password')

    def clean(self):
        cleaned_data = super(Addadminform, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        mobile = cleaned_data.get("mobile")
        if password != confirm_password:
            raise forms.ValidationError(
                ugettext("password and confirm password does not match")
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
               ugettext("username already exist")
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
               ugettext("Email already exist")
            )
        if User.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError(
               ugettext("Mobile number already exist")
            )
        return cleaned_data

class Loginform(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password','email')

    def clean(self):
        cleaned_data = super(Loginform, self).clean()
        email = cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
               ugettext("User is not Valid")
            )

class Edituserform(forms.Form):
    account_id = forms.IntegerField(required=True)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    date = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    status = forms.CharField(required=True)
    userimg = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username','account_id','first_name','last_name','mobile','date','email','status','userimg')

    def clean(self):
        cleaned_data = super(Edituserform, self).clean()
        username = cleaned_data.get("username")
        account_id = cleaned_data.get("account_id")

        if not User.objects.filter(username=username,account_id=account_id).exists():
            raise forms.ValidationError(
               ugettext("User is not Valid")
            )
        return cleaned_data

class ProfileForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    account_id = forms.IntegerField(required=True)
    mobile = forms.CharField()
    date = forms.CharField()
    userimg = forms.FileField(required=False)
    password = forms.CharField(required=False)
    confirm_password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'account_id', 'email', 'userimg')

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!=' ' and password!='' and password!=None:
            if confirm_password!=' ' and confirm_password!='' and confirm_password!=None:
                if password!=confirm_password:
                    raise forms.ValidationError(
                       ugettext("password and confirm password does not match")
                    )
            else:
                raise forms.ValidationError(
                   ugettext("confirm password feild is required")
                )

        return cleaned_data


class ForgetPassForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email')

    def clean(self):
        cleaned_data = super(ForgetPassForm, self).clean()
        email = cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
               ugettext("This email address does not exist in database.!")
            )

class ForgetpasswordForm(forms.Form):
    confirm_password = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('passowrd', 'confirm_password')

    def clean(self):
        cleaned_data = super(ForgetpasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password != password:
            raise forms.ValidationError(
               ugettext("Password And Confirm Password Not Match")
            )




from .models import AddGeneralsettingModel, SMTPdetailModel, SocialLinksmodel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher
User = get_user_model()
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class GeneralSettingForm(forms.Form):
    title = forms.CharField(required=True)
    Constant_Slug = forms.CharField(required=True)
    field_type = forms.CharField(required=True)
    setting_checkbox = forms.CharField(required=False)
    config_value = forms.CharField(required=False)

    class Meta:
        model = AddGeneralsettingModel
        fields = ('title', 'Constant_Slug', 'field_type', 'setting_checkbox')

    def clean(self):
        return super(GeneralSettingForm, self).clean()


class SMTPDetailform(forms.Form):
    SMTP_EMAIL = forms.EmailField(required=True)
    SMTPPASSWORD = forms.CharField(required=True)
    SMTPUSERNAME = forms.CharField(required=True)
    SMTPPORT = forms.IntegerField(required=True)

    class Meta:
        model = SMTPdetailModel
        fields = ("SMTP_EMAIL", "SMTPPASSWORD", "SMTPUSERNAME", "SMTPPORT")

    def clean(self):
        cleaned_data = super(SMTPDetailform, self).clean()
        return cleaned_data


class Sociallinkform(forms.Form):
    title = forms.CharField(required=True)
    url = forms.CharField(required=True)
    icon = forms.CharField(required=True)

    class Meta:
        model = SocialLinksmodel
        fields = ("title", "url", "iconclass")

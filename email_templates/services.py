from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime


class CreateEmailhookService(Service):
    title = forms.CharField()
    hook = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    status = forms.CharField()
    userid = forms.CharField()

    def process(self):
        Emailhookdb = AddEmailHooksModel(title=self.cleaned_data['title'],hook=self.cleaned_data['hook'],
                                         description=self.cleaned_data['description'],status=bool(self.cleaned_data['status']),
                                         userid=User.objects.get(username=self.cleaned_data['userid']))
        Emailhookdb.save()


class UpdateEmailhookService(Service):
    title = forms.CharField()
    hook = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    status = forms.CharField()
    id = forms.CharField()

    def process(self):
        Emailhookdb = AddEmailHooksModel.objects.get(id=self.cleaned_data['id'])
        Emailhookdb.title = self.cleaned_data['title']
        Emailhookdb.hook = self.cleaned_data['hook']
        Emailhookdb.description = self.cleaned_data['description']
        Emailhookdb.title = self.cleaned_data['title']
        Emailhookdb.updatedat = datetime.now()
        Emailhookdb.save()


class CreateMainEmailLayoutService(Service):
    title = forms.CharField()
    layout_html = forms.CharField(widget=forms.Textarea)
    user = forms.CharField()

    def process(self):
        MELdb = MainEmailLayoutModel(title=self.cleaned_data['title'],layout_html=self.cleaned_data['layout_html'],userid=User.objects.get(username=self.cleaned_data['user']))
        MELdb.save()


class EditMainEmailLayoutService(Service):
    title = forms.CharField()
    layout_html = forms.CharField(widget=forms.Textarea)
    user = forms.CharField()
    id = forms.CharField()

    def process(self):
        MELdb = MainEmailLayoutModel.objects.get(id=self.cleaned_data['id'])
        MELdb.title=self.cleaned_data['title']
        MELdb.layout_html=self.cleaned_data['layout_html']
        MELdb.userid=User.objects.get(username=self.cleaned_data['user'])
        MELdb.updatedat = datetime.now()
        MELdb.save()

class CreateEmailTemplateService(Service):
    emailhooks = forms.CharField()
    subject = forms.CharField()
    ckeditor = forms.CharField(widget=forms.Textarea)
    footer_text = forms.CharField()
    email_preference = forms.CharField()
    status = forms.CharField()
    user = forms.CharField()

    def process(self):
        EmailTemplatedb = EmailTemplateModel(emailhooks=AddEmailHooksModel.objects.get(title=self.cleaned_data['emailhooks']),
                                             subject=self.cleaned_data['subject'],
                                             ckeditor=self.cleaned_data['ckeditor'],
                                             footer_text=self.cleaned_data['footer_text'],
                                             email_preference=self.cleaned_data['email_preference'],
                                             status=bool(self.cleaned_data['status']),
                                             userid=User.objects.get(username=self.cleaned_data['user']))
        EmailTemplatedb.save()

class EditEmailTemplateService(Service):
    emailhooks = forms.CharField()
    subject = forms.CharField()
    ckeditor = forms.CharField(widget=forms.Textarea)
    footer_text = forms.CharField()
    email_preference = forms.CharField()
    status = forms.CharField()
    user = forms.CharField()
    id = forms.CharField()

    def process(self):
        EmailTemplatedb = EmailTemplateModel.objects.get(id=self.cleaned_data['id'])
        EmailTemplatedb.emailhooks = AddEmailHooksModel.objects.get(title=self.cleaned_data['emailhooks'])
        EmailTemplatedb.subject = self.cleaned_data['subject']
        EmailTemplatedb.ckeditor = self.cleaned_data['ckeditor']
        EmailTemplatedb.footer_text = self.cleaned_data['footer_text']
        EmailTemplatedb.email_preference = self.cleaned_data['email_preference']
        EmailTemplatedb.status = bool(self.cleaned_data['status'])
        EmailTemplatedb.updatedat = datetime.now()
        EmailTemplatedb.save()
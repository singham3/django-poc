from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from adminapp.hashers import *


class EditCMSPageService(Service):
    id = forms.CharField()
    title = forms.CharField()
    meta_title = forms.CharField()
    sub_title = forms.CharField()
    meta_keyword = forms.CharField()
    slug = forms.CharField()
    meta_description = forms.CharField()
    short_description = forms.CharField()
    cmsfile = forms.FileField(required=False)
    cktextarea = forms.CharField(widget=forms.Textarea)


    def process(self):
        cmsdata = CMSpagemodel.objects.get(id=self.cleaned_data['id'])
        cmsdata.title = self.cleaned_data['title']
        cmsdata.meta_title = self.cleaned_data['meta_title']
        cmsdata.sub_title = self.cleaned_data['sub_title']
        cmsdata.meta_keyword = self.cleaned_data['meta_keyword']
        cmsdata.slug = self.cleaned_data['slug']
        cmsdata.meta_description = self.cleaned_data['meta_description']
        cmsdata.short_description = self.cleaned_data['short_description']
        if self.cleaned_data['cmsfile']:
            cmsdata.cmsfile = self.cleaned_data['cmsfile']
        cmsdata.html_description = self.cleaned_data['cktextarea']
        cmsdata.updatedate = datetime.now()
        cmsdata.save()


class CreateCMSPageService(Service):
    title = forms.CharField()
    meta_title = forms.CharField()
    sub_title = forms.CharField()
    meta_keyword = forms.CharField()
    slug = forms.CharField()
    meta_description = forms.CharField()
    short_description = forms.CharField()
    cmsfile = forms.FileField()
    cktextarea = forms.CharField(widget=forms.Textarea)
    userid = forms.CharField()

    def process(self):
        cmsdb = CMSpagemodel(title=self.cleaned_data['title'], meta_title=self.cleaned_data['meta_title'], sub_title=self.cleaned_data['sub_title'],
                             meta_keyword=self.cleaned_data['meta_keyword'],slug=self.cleaned_data['slug'],
                             meta_description=self.cleaned_data['meta_description'],short_description=self.cleaned_data['short_description'],
                             cmsfile=self.cleaned_data['cmsfile'], html_description=self.cleaned_data['cktextarea'],
                             userid=User.objects.get(username=self.cleaned_data['userid']))
        cmsdb.save()
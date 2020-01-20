from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from adminapp.hashers import *


class CreateFavLgoService(Service):
    slug = forms.CharField()
    title = forms.CharField()
    field_type = forms.CharField()
    manager = forms.CharField()
    favlogo_value = forms.CharField()
    config_value_file = forms.FileField(required=False)
    userid = forms.CharField()

    def process(self):
        if LogoFavIconsModel.objects.filter(favlogo_value=self.cleaned_data['favlogo_value']).exists():
            lfdata = LogoFavIconsModel.objects.get(favlogo_value=self.cleaned_data['favlogo_value'])
            lfdata.slug = self.cleaned_data['slug']
            lfdata.title = self.cleaned_data['title']
            lfdata.field_type = self.cleaned_data['field_type']
            lfdata.manager = self.cleaned_data['manager']
            lfdata.updatedat = datetime.now()
            if self.cleaned_data['config_value_file']:
                lfdata.config_value_file = self.cleaned_data['config_value_file']
            lfdata.save()
        else:
            lfdb = LogoFavIconsModel(slug=self.cleaned_data['slug'], title=self.cleaned_data['title'],
                                     favlogo_value=self.cleaned_data['favlogo_value'],
                                     field_type=self.cleaned_data['field_type'],
                                     manager=self.cleaned_data['manager'], config_value_file=self.cleaned_data['config_value_file'],
                                     userid=User.objects.get(username=self.cleaned_data['userid']))
            lfdb.save()


class CreateGenSettingService(Service):
    title = forms.CharField()
    Constant_Slug = forms.CharField()
    field_type = forms.CharField()
    config_value = forms.CharField(widget=forms.Textarea,required=False)
    userid = forms.CharField()

    def process(self):
        if self.cleaned_data['config_value'] is None:
            AddGeneralsettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=False,
                                                  config_value_text=None,
                                                  userid=User.objects.get(username=self.cleaned_data['userid'])
                                                  )
        elif self.cleaned_data['config_value'] == "on":
            AddGeneralsettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=True,
                                                  config_value_text=None,
                                                  userid=User.objects.get(username=self.cleaned_data['userid'])
                                                  )
        else:
            AddGeneralsettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=None,
                                                  config_value_text=self.cleaned_data['config_value'],
                                                  userid=User.objects.get(username=self.cleaned_data['userid'])
                                                  )


class EditGenSettingService(Service):
    title = forms.CharField()
    Constant_Slug = forms.CharField()
    field_type = forms.CharField()
    config_value = forms.CharField(widget=forms.Textarea,required=False)
    settingid = forms.CharField()

    def process(self):
        GenSetdb = AddGeneralsettingModel.objects.get(id=self.cleaned_data['settingid'])
        GenSetdb.title = self.cleaned_data['title']
        GenSetdb.Constant_Slug = self.cleaned_data['Constant_Slug']
        GenSetdb.field_type = self.cleaned_data['field_type']
        if self.cleaned_data['config_value'] is None:
            GenSetdb.config_value_bool = False
        elif self.cleaned_data['config_value'] == "on":
            GenSetdb.config_value_bool = True
        else:
            GenSetdb.config_value_text = self.cleaned_data['config_value']
            GenSetdb.config_value_bool = None
        GenSetdb.updatedat = datetime.now()
        GenSetdb.save()


class SMTPdetailService(Service):
    SMTP_EMAIL = forms.EmailField()
    SMTPPASSWORD = forms.CharField()
    SMTPPORT = forms.IntegerField()
    SMTPUSERNAME = forms.CharField()
    userid = forms.CharField()

    def process(self):
        try:
            smtpdb = SMTPdetailModel.objects.get()
            smtpdb.SMTP_EMAIL = self.cleaned_data['SMTP_EMAIL']
            smtpdb.SMTPPASSWORD = encrypt_message_rsa(self.cleaned_data['SMTPPASSWORD'], jsondata["publickey"])
            smtpdb.SMTPPORT = self.cleaned_data['SMTPPORT']
            smtpdb.SMTPUSERNAME = self.cleaned_data['SMTPUSERNAME']
            smtpdb.userid = User.objects.get(username=self.cleaned_data['userid'])
            smtpdb.save()
        except:
            smtpdb = SMTPdetailModel(SMTP_EMAIL=self.cleaned_data['SMTP_EMAIL'],
                                     SMTPPASSWORD=encrypt_message_rsa(self.cleaned_data['SMTPPASSWORD'],
                                                                      jsondata["publickey"]),
                                     SMTPPORT=self.cleaned_data['SMTPPORT'],
                                     SMTPUSERNAME=self.cleaned_data['SMTPUSERNAME'],
                                     userid =User.objects.get(username=self.cleaned_data['userid']),)
            smtpdb.save()


class SocialLinkService(Service):
    userid = forms.CharField()
    title = forms.CharField()
    social_value = forms.CharField()
    url = forms.CharField()
    iconclass = forms.CharField()
    field_type = forms.CharField()
    manager = forms.CharField()

    def process(self):
        if SocialLinksmodel.objects.filter(social_value=self.cleaned_data['social_value']).exists():
            sldata = SocialLinksmodel.objects.get(social_value=self.cleaned_data['social_value'])
            sldata.title = self.cleaned_data['title']
            sldata.field_type = self.cleaned_data['field_type']
            sldata.manager = self.cleaned_data['manager']
            sldata.url = self.cleaned_data['url']
            sldata.iconclass = self.cleaned_data['iconclass']
            sldata.updateat = datetime.now()
            sldata.save()
        else:
            SocialLinksmodel.objects.create(userid=User.objects.get(username=self.cleaned_data['userid']),
                                            title=self.cleaned_data['title'],
                                            url=self.cleaned_data['url'],
                                            iconclass=self.cleaned_data['iconclass'],
                                            field_type=self.cleaned_data['field_type'],
                                            manager=self.cleaned_data['manager'],
                                            social_value=self.cleaned_data['social_value'])

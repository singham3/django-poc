from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class SettingsConfig(AppConfig):
    name = 'settings'


userjsondata = eval(open("config/adminappconfig/userconfig.json","r").read())
generalsettingjsondata = eval(open("config/settingconfig/generalsettingconfig.json","r").read())
LogoFavIconsjsondata = eval(open("config/settingconfig/LogoFavIconsconfig.json","r").read())
SocialLinksjsondata = eval(open("config/settingconfig/SocialLinksconfig.json","r").read())


def create_settings(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        userdata = User.objects.get(username="admin")
    except User.DoesNotExist:
        User.objects.create_superuser(username=userjsondata['username'], email=userjsondata['email'],
                                      first_name=userjsondata['first_name'], last_name=userjsondata['last_name'],
                                      is_superuser=bool(userjsondata['is_superuser']),
                                      is_staff=bool(userjsondata['is_staff']),
                                      is_active=bool(userjsondata['is_active']), mobile=userjsondata['mobile'],
                                      dateofbirth=datetime.strptime(userjsondata['dateofbirth'], '%m/%d/%Y'),
                                      userimg=userjsondata['userimg'],
                                      loginBrowser=userjsondata['loginBrowser'], loginip=str(IPAddr),
                                      account_id=randint(10 ** (8 - 1), (10 ** 8) - 1),
                                      password=userjsondata['password'])
        userdata = User.objects.get(username="admin")

    from .models import SMTPdetailModel, AddGeneralsettingModel,LogoFavIconsModel,SocialLinksmodel

    try:
        SMTPdetailModel.objects.get()
    except SMTPdetailModel.DoesNotExist:
        SMTPdetailModel.objects.create(userid=userdata)

    try:
        AddGeneralsettingModel.objects.get()
    except AddGeneralsettingModel.DoesNotExist:
        AddGeneralsettingModel.objects.create(title=generalsettingjsondata['title'],Constant_Slug=generalsettingjsondata['Constant_Slug'],
                                               field_type=generalsettingjsondata['field_type'],config_value_bool=None,
                                               config_value_text=generalsettingjsondata['config_value_text'],userid=userdata)

    try:
        LogoFavIconsModel.objects.get()
    except LogoFavIconsModel.DoesNotExist:
        LogoFavIconsModel.objects.create(slug=LogoFavIconsjsondata['MAIN_LOGO']['slug'],title=LogoFavIconsjsondata['MAIN_LOGO']['title'],
                                         field_type=LogoFavIconsjsondata['MAIN_LOGO']['field_type'],
                                         manager=LogoFavIconsjsondata['MAIN_LOGO']['manager'],
                                         favlogo_value=LogoFavIconsjsondata['MAIN_LOGO']['favlogo_value'],
                                         config_value_file=LogoFavIconsjsondata['MAIN_LOGO']['config_value_file'],
                                         userid=userdata)
        LogoFavIconsModel.objects.create(slug=LogoFavIconsjsondata['MAIN_FAVICON']['slug'],title=LogoFavIconsjsondata['MAIN_FAVICON']['title'],
                                         field_type=LogoFavIconsjsondata['MAIN_FAVICON']['field_type'],
                                         manager=LogoFavIconsjsondata['MAIN_FAVICON']['manager'],
                                         favlogo_value=LogoFavIconsjsondata['MAIN_FAVICON']['favlogo_value'],
                                         config_value_file=LogoFavIconsjsondata['MAIN_FAVICON']['config_value_file'],userid=userdata)

    try:
        SocialLinksmodel.objects.get()
    except SocialLinksmodel.DoesNotExist:
        SocialLinksmodel.objects.create(userid=userdata,title=SocialLinksjsondata['title'],url=SocialLinksjsondata['url'],
                                        social_value=SocialLinksjsondata['social_value'],manager=SocialLinksjsondata['manager'],
                                        iconclass=SocialLinksjsondata['iconclass'],field_type=SocialLinksjsondata['field_type'])


class settingsConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_settings)




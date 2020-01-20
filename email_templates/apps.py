from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class EmailTemplatesConfig(AppConfig):
    name = 'email_templates'



emailtemplatesjsondata = eval(open("config/emailtamplateconfig/emailtemplateconfig.json","r").read())
emailhooksjsondata = eval(open("config/emailtamplateconfig/emailhooksconfig.json","r").read())
mainemaillayoutjsondata = eval(open("config/emailtamplateconfig/mainemaillayoutconfig.json","r").read())
userjsondata = eval(open("config/adminappconfig/userconfig.json","r").read())

def create_emailtemplates(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from .models import EmailTemplateModel,MainEmailLayoutModel,AddEmailHooksModel
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        userdata = User.objects.get(username="admin")
    except User.DoesNotExist:
        User.objects.create_superuser(username=userjsondata['username'], email=userjsondata['email'],first_name=userjsondata['first_name'], last_name=userjsondata['last_name'],
                                      is_superuser=bool(userjsondata['is_superuser']),is_staff=bool(userjsondata['is_staff']),
                                      is_active=bool(userjsondata['is_active']), mobile=userjsondata['mobile'],dateofbirth=datetime.strptime(userjsondata['dateofbirth'], '%m/%d/%Y'),
                                      userimg=userjsondata['userimg'],loginBrowser=userjsondata['loginBrowser'], loginip=str(IPAddr),
                                      account_id=randint(10 ** (8 - 1), (10 ** 8) - 1),password=userjsondata['password'])
        userdata = User.objects.get(username="admin")

    try:
        emailhooks = AddEmailHooksModel.objects.get()
    except AddEmailHooksModel.DoesNotExist:
        AddEmailHooksModel.objects.create(title=emailhooksjsondata['title'], hook=emailhooksjsondata['hook'],
                                          description=emailhooksjsondata['description'], userid=userdata)
        emailhooks = AddEmailHooksModel.objects.get()

    try:
        EmailTemplateModel.objects.get()
    except EmailTemplateModel.DoesNotExist:
        EmailTemplateModel.objects.create(emailhooks=emailhooks,subject=emailtemplatesjsondata['subject'],
                                          ckeditor=emailtemplatesjsondata['ckeditor'],footer_text=emailtemplatesjsondata['footer_text'],
                                          email_preference=emailtemplatesjsondata['email_preference'],userid=userdata)

    try:
        MainEmailLayoutModel.objects.get()
    except MainEmailLayoutModel.DoesNotExist:
        MainEmailLayoutModel.objects.create(title=mainemaillayoutjsondata['title'],
                                            layout_html=mainemaillayoutjsondata['layout_html'],userid=userdata)




class emailtemplatesConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_emailtemplates)




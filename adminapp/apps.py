from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class AdminappConfig(AppConfig):
    name = 'adminapp'



userjsondata = eval(open("config/adminappconfig/userconfig.json","r").read())

def create_test_user(sender, **kwargs):
    if not settings.DEBUG:
        return
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    User = get_user_model()
    manager = User.objects
    try:
        manager.get(username="admin")
    except User.DoesNotExist:
        manager.create_superuser(username=userjsondata['username'], email=userjsondata['email'],
                                 first_name=userjsondata['first_name'], last_name=userjsondata['last_name'],
                                 is_superuser=bool(userjsondata['is_superuser']),
                                 is_staff=bool(userjsondata['is_staff']), is_active=bool(userjsondata['is_active']),
                                 mobile=userjsondata['mobile'],
                                 dateofbirth=datetime.strptime(userjsondata['dateofbirth'], '%m/%d/%Y'),
                                 userimg=userjsondata['userimg'],
                                 loginBrowser=userjsondata['loginBrowser'], loginip=str(IPAddr),
                                 account_id=randint(10 ** (8 - 1), (10 ** 8) - 1),password=userjsondata['password'])



class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)

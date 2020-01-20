from settings.models import *
from django.utils.translation import ugettext
import logging
import logging

logging.basicConfig(filename="debug/debug.log",
                    format='%(asctime)s %(name)-15s %(levelname)-5s %(message)s : [%(pathname)s line %(lineno)d, in %(funcName)s ]',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# logger = logging.getLogger(__name__)


cmsjsondata = eval(open("config/projectconfig/projectconfig.json", "r").read())



def AdminInfo(user):
    if User.objects.filter(username=user).exists():
        if LogoFavIconsModel.objects.filter(slug='MAIN_LOGO').exists():
            if LogoFavIconsModel.objects.filter(slug='MAIN_FAVICON').exists():
                return {"username":  User.objects.get(username=user),  "MAIN_FAVICON":  LogoFavIconsModel.objects.get(slug='MAIN_FAVICON'),
                           "MAIN_LOGO":  LogoFavIconsModel.objects.get(slug='MAIN_LOGO')}
            else:
                return {"username":  User.objects.get(username=user),  "MAIN_LOGO":  LogoFavIconsModel.objects.get(slug='MAIN_LOGO')}
        else:
            return {"username":  User.objects.get(username=user)}
    else:
        if LogoFavIconsModel.objects.filter(slug='MAIN_LOGO').exists():
            if LogoFavIconsModel.objects.filter(slug='MAIN_FAVICON').exists():
                return {"MAIN_FAVICON":  LogoFavIconsModel.objects.get(slug='MAIN_FAVICON'), "MAIN_LOGO":  LogoFavIconsModel.objects.get(slug='MAIN_LOGO')}
            else:
                return {"MAIN_LOGO":  LogoFavIconsModel.objects.get(slug='MAIN_LOGO')}
        else:
            return None
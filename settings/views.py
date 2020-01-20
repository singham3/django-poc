from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from datetime import datetime, date
from POC.admininfo import *
from django.template.response import TemplateResponse
from django.utils.decorators import decorator_from_middleware
from ipware import get_client_ip
from django.http import HttpResponse
from .middleware import *
from adminapp.hashers import *
from .services import *
from django.utils.translation import ugettext
from django.utils.translation import activate,  get_language
from django.core.paginator import Paginator


def allLogoFavIcons(page):
    try:
        allLogoFavIcons = LogoFavIconsModel.objects.all()
        paginator = Paginator(allLogoFavIcons, 10)
        contacts = paginator.get_page(page)
        return contacts, contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None,None,e

def allGeneralSettings(page):
    try:
        allGeneralSetting = AddGeneralsettingModel.objects.all()
        paginator = Paginator(allGeneralSetting, 10)
        contacts = paginator.get_page(page)
        return contacts, contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None,None,e

def allsociallinks(page):
    try:
        allsociallink = SocialLinksmodel.objects.all()
        paginator = Paginator(allsociallink, 10)
        contacts = paginator.get_page(page)
        return contacts, contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


@decorator_from_middleware(FavLogoAddMiddleware)
def AddLogoFavicon(request, page=1):
    if LogoFavIconsModel.objects.count() == 1:
            lastdata = LogoFavIconsModel.objects.get()
            lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0])+1
    elif LogoFavIconsModel.objects.count() == 0:
        lastid = 1
    else:
        lastdata = LogoFavIconsModel.objects.last()
        lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0])+1
    try:
        if request.method == "POST":
            postdata = [i for i in request.POST.keys()]
            postdata.extend([i for i in request.FILES.keys()])
            postdata.remove("csrfmiddlewaretoken")
            keyset = set()
            for l in postdata:
                keyset.add(l[0: -1].split("[")[0])
            keyset = list(keyset)
            allkeys = []
            for ks in keyset:
                samekeys = []
                for lst in postdata:
                    if ks in lst:
                        samekeys.append(lst)
                allkeys.append(samekeys)
            for postkey in allkeys:
                if postkey[5] in request.FILES:
                    CreateFavLgoService.execute({
                        "slug": request.POST.get(postkey[0]),
                        "title": request.POST.get(postkey[1]),
                        "field_type": request.POST.get(postkey[2]),
                        "manager": request.POST.get(postkey[3]),
                        "favlogo_value": request.POST.get(postkey[4]),
                        "userid": request.user
                    }, {"config_value_file": request.FILES[postkey[5]]})
                else:

                    CreateFavLgoService.execute({
                        "slug": request.POST.get(postkey[0]),
                        "title": request.POST.get(postkey[1]),
                        "field_type": request.POST.get(postkey[2]),
                        "manager": request.POST.get(postkey[3]),
                        "favlogo_value": request.POST.get(postkey[4]),
                        "userid": request.user
                    })
            lastid = LogoFavIconsModel.objects.last()
            allFIs = allLogoFavIcons(page)
            logger.error("Logo/Fav Icon id {} Successfully Updated".format(lastid.id))
            return TemplateResponse(request, "adminapp/pages/examples/favandlogo.html",
                                    {"flset": "active", "ificon": AdminInfo(request.user),
                                     "lastid":  lastid, "alllfdata":  allFIs[0],
                                     "range": allFIs[1], "error": allFIs[2],
                                     "msg":  ugettext("Successfully Updated")})
    except Exception as e:
        logger.error(e)
        allfis = allLogoFavIcons(page)
        return TemplateResponse(request, "adminapp/pages/examples/favandlogo.html",
                                {"flset": "active", "username": request.user, "ificon": AdminInfo(request.user),
                                 "lastid": lastid, "alllfdata": allfis[0], "range": allfis[1],
                                 "error": e if allfis[2] else e}, status=500)


class LogoFavDelete(APIView):
    def post(self, request):
        try:
            if 'slugid' in request.data and request.data['slugid']:
                if LogoFavIconsModel.objects.filter(favlogo_value=request.data['slugid']).exists():
                    settingdata = LogoFavIconsModel.objects.get(favlogo_value=request.data['slugid'])
                    settingdata.delete()
                    return HttpResponse(json.dumps({"msg": ugettext("Successfully Deleted")}), content_type="application/json")
                else:
                    logger.error(ugettext("Logo/Fav id {} not found".format(request.data['slugid'])))
                    return render(request, 'adminapp/pages/examples/404.html', {"ificon": AdminInfo(request.user)}, status= 404)
            else:
                logger.error(ugettext("Logo/Fav id {} not found".format(request.data['slugid'])))
                return render(request, 'adminapp/pages/examples/404.html', {"ificon": AdminInfo(request.user)}, status=404)
        except Exception as e:
            logger.error(e)


@decorator_from_middleware(GeneralSettingMiddleware)
def Generalform(request, page=1):
    if request.method == "POST":
        try:
            CreateGenSettingService.execute({
                "title": request.POST.get("title"),
                "Constant_Slug": request.POST.get("Constant_Slug"),
                "field_type": request.POST.get("field_type"),
                "setting_checkbox": request.POST.get("setting_checkbox"),
                "config_value": request.POST.get("config_value"),
                "userid": request.user
            })
            lastid = AddGeneralsettingModel.objects.last()
            logger.info("New General Setting id {} Successfully Added".format(lastid.id))
            allGS = allGeneralSettings(page)
            return TemplateResponse(request, "adminapp/pages/tables/simple2.html",
                                    {"genset": "active", "ificon": AdminInfo(request.user), "allGS": allGS[0],
                                     "range": allGS[1], "error": allGS[2]})
        except Exception as e:
            logger.error(e)
            allGS = allGeneralSettings(page)
            return TemplateResponse(request, "adminapp/pages/tables/simple2.html",
                                    {"genset": "active", "ificon": AdminInfo(request.user),
                                     "allGS": allGS[0], "range": allGS[1], "error": e if allGS[2] else e}, status=500)


@decorator_from_middleware(ViewGeneralSettingMiddleware)
def ViewGeneralSettings(request, id,page=1):
    try:
        settingdata = AddGeneralsettingModel.objects.get(id=id)
        return TemplateResponse(request, "adminapp/pages/examples/viewgeneralsettings.html",{"genset":"active","ificon": AdminInfo(request.user), "settingdata": settingdata})
    except Exception as e:
        logger.error(e)
        allGS = allGeneralSettings(page)
        return TemplateResponse(request, "adminapp/pages/tables/simple2.html",{"genset": "active", "ificon": AdminInfo(request.user),"allGS": allGS[0],"range":allGS[1],"error":e if allGS[2] else e}, status=500)


@decorator_from_middleware(EditGeneralSettingMiddleware)
def Editgeneralsettings(request, form, id):
    if request.method == "POST":
        try:
            EditGenSettingService.execute({
                "title": form.cleaned_data.get("title"),
                "Constant_Slug": form.cleaned_data.get("Constant_Slug"),
                "field_type": form.cleaned_data.get("field_type"),
                "setting_checkbox": form.cleaned_data.get("setting_checkbox"),
                "config_value": form.cleaned_data.get("config_value"),
                "settingid": id
            })
            logger.info("General Setting id {} Successfully Updated".format(id))
            return TemplateResponse(request, "adminapp/pages/examples/editsettings.html",{"genset":"active","ificon": AdminInfo(request.user), "settingdata": AddGeneralsettingModel.objects.get(id=id),"msg": ugettext("Successfully Updated")})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/examples/editsettings.html",{"genset":"active","ificon": AdminInfo(request.user), "settingdata": AddGeneralsettingModel.objects.get(id=id),"error": e},status=500)


@decorator_from_middleware(AddGeneralSettingMiddleware)
def AddGeneralsetting(request):
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get("config_value"))
        try:
            CreateGenSettingService.execute({
                "title": request.POST.get("title"),
                "Constant_Slug": request.POST.get("Constant_Slug"),
                "field_type": request.POST.get("field_type"),
                "setting_checkbox": request.POST.get("setting_checkbox"),
                "config_value": request.POST.get("config_value"),
                "userid": request.user
            })
            lastid = AddGeneralsettingModel.objects.last()
            logger.info("New General Setting id {} Successfully Added".format(lastid.id))
            return TemplateResponse(request, "adminapp/pages/examples/addsettings.html",{"genset":"active","ificon": AdminInfo(request.user)})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/examples/addsettings.html", {"genset":"active","ificon": AdminInfo(request.user), "error": e},status=500)


@decorator_from_middleware(SMTPdeatilsMiddleware)
def SMTPdeatils(request, form):
    if request.method == "POST":
        print(request.POST)
        try:
            smtpdb = SMTPdetailModel.objects.get()
        except:
            smtpdb = None
        try:
            SMTPdetailService.execute({
                "SMTP_EMAIL": form.cleaned_data.get("SMTP_EMAIL"),
                "SMTPPASSWORD": form.cleaned_data.get("SMTPPASSWORD"),
                "SMTPPORT": form.cleaned_data.get("SMTPPORT"),
                "SMTPUSERNAME": form.cleaned_data.get("SMTPUSERNAME"),
                "userid": request.user
            })
            logger.info("SMTP Deatils Successfully Updated")
            return TemplateResponse(request, "adminapp/pages/examples/SMTPdetails.html",
                                    {"smtpset": "active", "ificon": AdminInfo(request.user),
                                     "msg": ugettext("Successfully Updated"), "smtpdata": SMTPdetailModel.objects.get(),
                                     "smtppass": decrypt_message_rsa(smtpdb.SMTPPASSWORD, jsondata["privatekey"])})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/examples/SMTPdetails.html",
                                    {"smtpset": "active", "ificon": AdminInfo(request.user), "error": e,
                                     "smtpdata": smtpdb,
                                     "smtppass": decrypt_message_rsa(smtpdb.SMTPPASSWORD, jsondata["privatekey"])},
                                    status=500)


@decorator_from_middleware(AddsociallinsMiddleware)
def Addsociallins(request, page=1):
    if SocialLinksmodel.objects.count() == 1:
        lastdata = SocialLinksmodel.objects.get()
        lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
    elif SocialLinksmodel.objects.count() == 0:
        lastid = 1
    else:
        lastdata = SocialLinksmodel.objects.last()
        lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
    if request.method == "POST":
        try:
            print(request.POST)
            requestdata = dict(request.POST)
            title = requestdata['title']
            field_type = requestdata['field_type']
            manager = requestdata['manager']
            url = requestdata['url']
            icon = requestdata['icon']
            social_value = requestdata["social-value"]
            for i in range(len(title)):
                SocialLinkService.execute({
                    "userid": request.user,
                    "title": title[i],
                    "social_value": social_value[i],
                    "url": url[i],
                    "iconclass": icon[i],
                    "field_type": field_type[i],
                    "manager": manager[i]
                })
            logger.info("Social link Successfully Updated")
            allsociallink = allsociallinks(page)
            return render(request, "adminapp/pages/examples/addsociallinks.html",{"socset":"active","ificon": AdminInfo(request.user), "msg": ugettext("Successfully Updated"),"allsociallinks": allsociallink[0],"range":allsociallink[1],"error":allsociallink[2],"lastid": lastid})
        except Exception as e:
            logger.error(e)
            allsociallink = allsociallinks(page)
            return render(request, "adminapp/pages/examples/addsociallinks.html",{"socset":"active","ificon": AdminInfo(request.user), "allsociallinks": allsociallink[0],"range":allsociallink[1],"error":e if allsociallink[2] else e, "lastid": lastid})


class Deletesociallins(APIView):
    def post(self, request):
        try:
            if 'slid' in request.data and request.data['slid']:
                if SocialLinksmodel.objects.filter(id=request.data['slid']).exists():
                    settingdata = SocialLinksmodel.objects.get(id=request.data['slid'])
                    settingdata.delete()
                    return HttpResponse(json.dumps({"msg": "Successfully Deleted"}), content_type="application/json")
                else:
                    logger.error(ugettext("Social Link id {} not found".format(request.data['slugid'])))
                    return render(request, 'adminapp/pages/examples/404.html', {"ificon": AdminInfo(request.user)},status=404)
            else:
                logger.error(ugettext("Social Link id {} not found".format(request.data['slugid'])))
                return render(request, 'adminapp/pages/examples/404.html', {"ificon": AdminInfo(request.user)}, status=404)
        except Exception as e:
            logger.error(e)



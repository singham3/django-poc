from django.shortcuts import render
from django.shortcuts import redirect
from adminapp.token_auth import *
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login, ImproperlyConfigured
from django.http import HttpResponse
from django.urls import resolve
from .forms import *
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django import http
import sys
from POC.admininfo import *
from adminapp.hashers import *


class FavLogoAddMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if LogoFavIconsModel.objects.count() == 1:
            lastdata = LogoFavIconsModel.objects.get()
            lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0]) + 1
        elif LogoFavIconsModel.objects.count() == 0:
            lastid = 1
        else:
            lastdata = LogoFavIconsModel.objects.last()
            lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0]) + 1
        if request.method == "POST":
            return None
        return render(request, "adminapp/pages/examples/favandlogo.html", {"flset":"active","ificon": AdminInfo(request.user), "lastid": lastid, "alllfdata": LogoFavIconsModel.objects.all()})

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class GeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = GeneralSettingForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/tables/simple2.html",
                              {"genset": "active", "ificon": AdminInfo(request.user), "form": form,
                               "allGS": AddGeneralsettingModel.objects.all()})
        return render(request, "adminapp/pages/tables/simple2.html",
                      {"genset": "active", "ificon": AdminInfo(request.user),
                       "allGS": AddGeneralsettingModel.objects.all()})

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class ViewGeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' not in view_kwargs and not view_kwargs['id']:
            if not AddGeneralsettingModel.objects.filter(id=view_kwargs['id']).exists():
                logger.error("General Setting id {} not found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"genset":"active","ificon": AdminInfo(request.user)},status=404)
            logger.error("General Setting id {} not found".format(view_kwargs['id']))
            return render(request, 'adminapp/pages/examples/404.html', {"genset":"active","ificon": AdminInfo(request.user)}, status=404)


class EditGeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' in view_kwargs and view_kwargs['id']:
            if AddGeneralsettingModel.objects.filter(id=view_kwargs['id']).exists():
                settingdata = AddGeneralsettingModel.objects.get(id=view_kwargs['id'])
                if request.method == "POST":
                    form = GeneralSettingForm(request.POST)
                    if not form.is_valid():
                        logger.error(form.errors)
                        logger.error(form.non_field_errors)
                        return render(request, "adminapp/pages/examples/editsettings.html",
                                      {"genset": "active","ificon": AdminInfo(request.user), "settingdata": settingdata,
                                       "form": form})
                    else:
                        return view_func(request, form, view_kwargs['id'])
                return render(request, "adminapp/pages/examples/editsettings.html", {"genset":"active","ificon": AdminInfo(request.user), "settingdata": settingdata})
            else:
                logger.error("General Setting id {} not found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"genset":"active","ificon": AdminInfo(request.user)}, status=404)
        else:
            logger.error("General Setting id {} not found".format(view_kwargs['id']))
            return render(request, 'adminapp/pages/examples/404.html', {"genset":"active","ificon": AdminInfo(request.user)}, status=404)


class AddGeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = GeneralSettingForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/addsettings.html", {"genset":"active","ificon": AdminInfo(request.user),"form":form})
            else:
                return None
        return render(request, "adminapp/pages/examples/addsettings.html",{"genset": "active", "ificon": AdminInfo(request.user)})


class SMTPdeatilsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            smtpdb = SMTPdetailModel.objects.get()
        except:
            smtpdb = None
        if request.method == "POST":
            form = SMTPDetailform(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/SMTPdetails.html",
                              {"smtpset":"active","ificon": AdminInfo(request.user), "form": form, "smtpdata": smtpdb,
                               "smtppass": decrypt_message_rsa(smtpdb.SMTPPASSWORD, jsondata["privatekey"])})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/examples/SMTPdetails.html",
                      {"smtpset":"active","ificon": AdminInfo(request.user), "smtpdata": smtpdb,
                       "smtppass": decrypt_message_rsa(smtpdb.SMTPPASSWORD, jsondata["privatekey"])})


class AddsociallinsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if SocialLinksmodel.objects.count() == 1:
            lastdata = SocialLinksmodel.objects.get()
            lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
        elif SocialLinksmodel.objects.count() == 0:
            lastid = 1
        else:
            lastdata = SocialLinksmodel.objects.last()
            lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
        if request.method == "POST":
            form = Sociallinkform(request.POST, request.FILES)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/addsociallinks.html",
                              {"socset":"active","ificon": AdminInfo(request.user), "form": form,"allsociallinks": SocialLinksmodel.objects.all(), "lastid": lastid})
            else:
                return None
        return render(request, "adminapp/pages/examples/addsociallinks.html",
                      {"socset":"active","username": request.user, "ificon": AdminInfo(request.user), "lastid": lastid,
                       "allsociallinks": SocialLinksmodel.objects.all()})



from django.shortcuts import render
from django.shortcuts import redirect
from .token_auth import *
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login, ImproperlyConfigured
from django.http import HttpResponse
from django.urls import resolve
from .forms import *
from django.http import HttpResponse
from django.conf import settings
from django import http
import sys
from POC.admininfo import *
import jwt
from datetime import datetime,timedelta
from .hashers import *
from django.utils import translation

projectjsondata = eval(open("config/projectconfig/projectconfig.json", "r").read())
View_class = ['Login', 'ForgetPassword', 'Verifyforgetpass']


class StandardExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(exception)
        if request.user.is_authenticated and Token_authentigetion(request):
            return render(request, 'adminapp/pages/examples/500.html', {"ificon": AdminInfo(request.user),"error": exception, "status": 500}, status=500)
        return render(request,  'adminapp/pages/examples/changepasserror.html', {"error": exception, "status": 500}, status=500)


class HomeMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        translation.activate("".join(projectjsondata["language_code"]))
        if view_func.__name__ in View_class:
            if request.user.is_authenticated and Token_authentigetion(request):
                return redirect("/dashboard/")
        else:
            if not hasattr(request, 'user'):
                return redirect("/")
            if not request.user.is_authenticated and not Token_authentigetion(request):
                if 'csrftoken' in request.COOKIES:
                    request.COOKIES.pop("csrftoken")
                if 'sessionid' in request.COOKIES:
                    request.COOKIES.pop("sessionid")
                logger.error("User is not authenticated")
                return redirect("/")


class ProfileMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        userprofiledata = User.objects.get(username=request.user)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/profile.html",
                              {"ificon": AdminInfo(request.user), "profiledata": userprofiledata,
                               "profiledate": userprofiledata.dateofbirth.strftime('%m/%d/%Y'),
                               "form": form})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/examples/profile.html",
                          {"username": User.objects.get(username=request.user), "ificon": AdminInfo(request.user),
                           "profiledata": userprofiledata, "profiledate": userprofiledata.dateofbirth.strftime('%m/%d/%Y')})

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response
        else:
            if 'csrftoken' in request.COOKIES:
                request.COOKIES.pop("csrftoken")
            if 'sessionid' in request.COOKIES:
                request.COOKIES.pop("sessionid")
            logger.error("User is not authenticated")
            return redirect("/")



class UserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = Addadminform(request.POST, request.FILES)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/adduser.html",{"userac":"active","form": form, "ificon": AdminInfo(request.user), "username": request.user})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/examples/adduser.html",{"userac":"active","ificon": AdminInfo(request.user)})

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class EditUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' in view_kwargs and view_kwargs['id']:
            if User.objects.filter(account_id=view_kwargs['id']).exists():
                user_data = User.objects.get(account_id=view_kwargs['id'])
                if request.method == "POST":
                    editform = Edituserform(request.POST, request.FILES)
                    if not editform.is_valid():
                        logger.error(editform.errors)
                        logger.error(editform.non_field_errors)
                        return render(request,  "adminapp/pages/examples/edituser.html",
                                      {"userac":"active","form":  editform, "ificon": AdminInfo(request.user), "edit_data":  User.objects.get(account_id=request.GET['id'])})
                    else:
                        return view_func(request,editform,view_kwargs['id'])
                return render(request, "adminapp/pages/examples/edituser.html",{"userac":"active","edit_data": user_data, "ificon": AdminInfo(request.user)})
            else:
                logger.error("This ID {} Not Found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"userac":"active","ificon": AdminInfo(request.user)},status=404)
        else:
            logger.error("This ID {} Not Found".format(view_kwargs['id']))
            return render(request, 'adminapp/pages/examples/404.html', {"userac":"active","ificon": AdminInfo(request.user)}, status=404)

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class ViewUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' not in view_kwargs and not view_kwargs['id']:
            if not User.objects.filter(account_id=view_kwargs['id']).exists():
                logger.error("This ID {} Not Found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"userac":"active","ificon": AdminInfo(request.user)},status=404)
            logger.error("This ID {} Not Found".format(view_kwargs['id']))
            return render(request, 'adminapp/pages/examples/404.html', {"userac":"active","ificon": AdminInfo(request.user)}, status=404)

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response




class AllUserMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class LoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            loginform = Loginform(request.POST)
            if not loginform.is_valid():
                logger.error(loginform.errors)
                logger.error(loginform.non_field_errors)
                return render(request,  "adminapp/pages/examples/login.html",  {"form":  loginform, "ificon": AdminInfo(request.user)})
            else:
                return None
        if request.user.is_authenticated and Token_authentigetion(request):
            return redirect('/dashboard/')
        else:
            return render(request, "adminapp/pages/examples/login.html", {"ificon": AdminInfo(request.user)})

    def process_template_response(self, request, response):
        return response


class ForgetPasswordMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = ForgetPassForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/examples/forgetpass.html",{"ificon": AdminInfo(request.user), "form": form})
            else:
                return None
        return render(request, "adminapp/pages/examples/forgetpass.html", {"ificon": AdminInfo(request.user)})

    def process_template_response(self, request, response):
        return response

class VerifyPasswordMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "token" in request.GET and request.GET['token']:
            token = request.GET['token']
            data = jwt.decode(token, jsondata["publickey"], 'utf-8')
            if datetime.now() - datetime.strptime(data["token_created_at"], '%Y-%m-%d %H:%M:%S.%f') < timedelta(hours=24, minutes=1):
                realdata = eval(decrypt_message_rsa(data["data"], jsondata["privatekey"]))
                if User.objects.filter(email=realdata[0], username=realdata[1], account_id=realdata[2],key=realdata[3]).exists():
                    if request.method == "POST":
                        form = ForgetpasswordForm(request.POST)
                        if not form.is_valid():
                            logger.error(form.errors)
                            logger.error(form.non_field_errors)
                            return render(request, 'adminapp/pages/examples/changepass.html',
                                                    {"ificon": AdminInfo(request.user), "form": form})
                        else:
                            return None
                    return render(request, 'adminapp/pages/examples/changepass.html',{"ificon": AdminInfo(request.user)})
            else:
                logger.error("URL time out")
                return render(request, 'adminapp/pages/examples/changepasserror.html',{"error": ugettext("URL time out"), "status": 404}, status=404)
        else:
            logger.error("Page not found.")
            return render(request, 'adminapp/pages/examples/changepasserror.html',{"error":ugettext("Page not found."), "status": 404}, status=404)


    def process_template_response(self, request, response):
        return response
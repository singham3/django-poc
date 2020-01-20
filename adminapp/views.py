from django.contrib.auth.models import User
from ipware import get_client_ip

from django.contrib import auth
from .emailsend import *
from .middleware import *
from django.utils.decorators import decorator_from_middleware
from django.template.response import TemplateResponse
from POC.admininfo import *
from email_templates.models import EmailTemplateModel
from CMSpages.models import CMSpagemodel
from .services import *

from django.core.paginator import Paginator


def all_users(page):
    try:
        all_user = User.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return contacts,contacts.paginator.page_range,None
    except Exception as e:
        logger.error(e)
        return None,None,e

def view_404(request, exception): 
    return render(request,  'adminapp/pages/examples/404.html', {"ificon": AdminInfo(request.user)},  status=404)

def view_500(request): 
    return render(request,  'adminapp/pages/examples/500.html', {"ificon": AdminInfo(request.user)},  status=500)

def Home(request):
    return render(request,  "adminapp/index.html", {"ificon": AdminInfo(request.user), "emailcount": EmailTemplateModel.objects.count(), "usercount": User.objects.count(), "cmspagescount": CMSpagemodel.objects.count()})


@decorator_from_middleware(ProfileMiddleware)
def Profile(request,form):
    if request.method == "POST":
        try:
            EditUserService.execute({
                "username": form.cleaned_data.get('username'),
                "first_name": form.cleaned_data.get('first_name'),
                "last_name": form.cleaned_data.get("last_name"),
                "mobile": form.cleaned_data.get("mobile"),
                "account_id": form.cleaned_data.get("account_id"),
                "date": form.cleaned_data.get("date"),
                "email": form.cleaned_data.get("email"),
                "status": form.cleaned_data.get("status"),
                "password": form.cleaned_data.get('password'),
                "browsertype": request.META['HTTP_USER_AGENT'],
                "userip": get_client_ip(request)[0],
            }, {"userimg": form.cleaned_data.get("userimg")})
            if form.cleaned_data.get('password'):
                logger.info("{} Successfully Profile Updated".format(form.cleaned_data.get("email")))
                return redirect("/logout/")
            logger.info("{} Successfully Profile Updated".format(form.cleaned_data.get("email")))
            return TemplateResponse(request,"adminapp/pages/examples/profile.html", {"ificon": AdminInfo(request.user), "profiledata":  User.objects.get(username=request.user),  "msg": ugettext("Successfully Update")})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/examples/profile.html", {"ificon": AdminInfo(request.user), "profiledata":  User.objects.get(username=request.user),  "error":  e})


@decorator_from_middleware(UserMiddleware)
def Adduser(request,form):
    if request.method == "POST":
        try:
            CreateUserService.execute({
                "username" : form.cleaned_data.get("username"),
                "first_name" : form.cleaned_data.get("first_name"),
                "last_name" : form.cleaned_data.get("last_name"),
                "mobile" : form.cleaned_data.get("mobile"),
                "date" : form.cleaned_data.get("date"),
                "email" : form.cleaned_data.get("email"),
                "status" : form.cleaned_data.get("status"),
                "password" : form.cleaned_data.get("password"),
                "browser_type" : request.META['HTTP_USER_AGENT'],
                "user_ip" : get_client_ip(request)[0]
            },{"userimg" : form.cleaned_data.get("userimg"),})
            logger.info("{} Successfully Created".format(form.cleaned_data.get("email")))
            return redirect("/users/pages/")
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/examples/adduser.html",  {"userac":"active","error":  e, "ificon":  AdminInfo(request.user), "username": request.user})

@decorator_from_middleware(EditUserMiddleware)
def Edituserdata(request,form,id):
    if request.method == "POST":
        try:
            EditUserService.execute({
                "username": form.cleaned_data.get('username'),
                "first_name": form.cleaned_data.get('first_name'),
                "last_name": form.cleaned_data.get("last_name"),
                "mobile": form.cleaned_data.get("mobile"),
                "account_id": id,
                "date": form.cleaned_data.get("date"),
                "email": form.cleaned_data.get("email"),
                "status": int(form.cleaned_data.get("status")),
                "browsertype": request.META['HTTP_USER_AGENT'],
                "userip": get_client_ip(request)[0],
            }, {"userimg": form.cleaned_data.get("userimg")})
            logger.info("{} Successfully Updated".format(form.cleaned_data.get("email")))
            return TemplateResponse(request,  "adminapp/pages/examples/edituser.html", {"userac":"active","msg": ugettext("Successfully Updated"), "ificon": AdminInfo(request.user),  "edit_data":  User.objects.get(account_id=id)})
        except Exception as e:
            logger.error(e)
            user_data = User.objects.get(account_id=int(id))
            return TemplateResponse(request,  "adminapp/pages/examples/edituser.html",{"userac":"active","error":  e,  "edit_data":  user_data, "ificon": AdminInfo(request.user)})

@decorator_from_middleware(ViewUserMiddleware)
def Viewuser(request, id,page=1):
    try:
        user_data = User.objects.get(account_id=id)
        return TemplateResponse(request, "adminapp/pages/examples/viewuser.html",
                  {"userac":"active","user_data": user_data, "ificon": AdminInfo(request.user)})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/tables/simple.html",
                                {"userac": "active", "ificon": AdminInfo(request.user),
                                 "all_user": all_users(page)[0],"range":all_users(page)[1],"error":e if all_users(page)[2] else e})


@decorator_from_middleware(ViewUserMiddleware)
def Deleteuser(request, id,page=1):
    try:
        user_data = User.objects.get(account_id=id)
        username = user_data.username
        user_data.delete()
        logger.info("{} Successfully Deleted".format(username))
        return TemplateResponse(request, "adminapp/pages/tables/simple.html",
                      {"userac":"active","ificon": AdminInfo(request.user),"all_user": all_users(page)[0],"range":all_users(page)[1],"error":all_users(page)[2], "msg": ugettext("Successfully Deleted")})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/tables/simple.html",
                                {"userac": "active", "ificon": AdminInfo(request.user),
                                 "all_user": all_users(page)[0],"range":all_users(page)[1],"error":e if all_users(page)[2] else e})

@decorator_from_middleware(AllUserMiddleware)
def Usertable(request,page=1):
    return TemplateResponse(request,  "adminapp/pages/tables/simple.html",  {"userac":"active","all_user": all_users(page)[0],
                                                                             "range":all_users(page)[1],"error":all_users(page)[2],
                                                                             "ificon": AdminInfo(request.user)})
    




@decorator_from_middleware(LoginMiddleware)
def Login(request):
    if request.method == "POST": 
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            browsertype = request.META['HTTP_USER_AGENT']
            try:
                allow = request.POST.get('checkbox')
            except:
                allow = None
            userip = get_client_ip(request)[0]
            if User.objects.filter(email=email).exists():
                userdata = User.objects.get(email=email)
                user = authenticate(username=userdata.username, password=password)
                if user is not None:
                    auth.login(request,  user)
                    userdata.loginBrowser = browsertype
                    userdata.loginip = userip
                    userdata.last_login = datetime.now()
                    userdata.key = None
                    userdata.save()
                    logger.info("{} Successfully Login".format(email))
                    return redirect('/dashboard/')
                else:
                    logger.error("Incorrect username and password")
                    return TemplateResponse(request,  "adminapp/pages/examples/login.html", {"error": ugettext("Please enter the correct username and password "), "ificon": AdminInfo(request.user)})
            else:
                logger.error("Invalid Username and Password")
                return TemplateResponse(request,  "adminapp/pages/examples/login.html",  {"error": ugettext("Invalid Username and Password"), "ificon": AdminInfo(request.user)})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/examples/login.html",  {"error":  e, "ificon": AdminInfo(request.user)})


@decorator_from_middleware(ForgetPasswordMiddleware)
def ForgetPassword(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                userdat = User.objects.get(email=email)
                responce = dict(Emailsend(userdat))
                userdat.updatedate = datetime.now()
                userdat.save()
                fp = {"ificon":  AdminInfo(request.user)}
                fp.update(responce)
                logger.info(responce)
                return TemplateResponse(request,  "adminapp/pages/examples/forgetpass.html", fp)
            else:
                logger.error("email not found")
                return TemplateResponse(request,  "adminapp/pages/examples/forgetpass.html",{"ificon":  AdminInfo(request.user),  "error": ugettext("email not found")})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/examples/forgetpass.html",{"ificon":  AdminInfo(request.user),  "error": e})

@decorator_from_middleware(VerifyPasswordMiddleware)
def Verifyforgetpass(request):
    try:
        token = request.GET['token']
        data = jwt.decode(token,  jsondata["publickey"], 'utf-8')
        if datetime.now() - datetime.strptime(str(data["token_created_at"]),  '%Y-%m-%d %H:%M:%S.%f') < timedelta(hours=24,  minutes=1):
            realdata = eval(decrypt_message_rsa(data["data"],  jsondata["privatekey"]))
            if User.objects.filter(email=realdata[0], username=realdata[1], account_id=realdata[2], key=realdata[3]).exists():
                userdata = User.objects.get(email=realdata[0], username=realdata[1], account_id=realdata[2], key=realdata[3])
                if request.method == "POST":
                    password = request.POST.get("password")
                    userdata.key = None
                    userdata.set_password(password)
                    userdata.save()
                    logger.info("{} Successfully Password Changed".format(realdata[0]))
                    return redirect('/')
            else:
                logger.error("User Details not Valid")
                return TemplateResponse(request,  'adminapp/pages/examples/changepasserror.html', {"error": ugettext("User Details not Valid"), "status": 404}, status=404)
        else:
            logger.error("Token Time Out")
            return TemplateResponse(request,  'adminapp/pages/examples/changepasserror.html', {"error":ugettext("Token Time Out"), "status": 500}, status=500)
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request,  'adminapp/pages/examples/changepasserror.html', {"error": e, "status": 500}, status=500)



def LogotView(request): 
    auth.logout(request)
    return redirect('/')




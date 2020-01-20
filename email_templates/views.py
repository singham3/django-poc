from django.shortcuts import render
from .models import *
from POC.admininfo import *
from django.template.response import TemplateResponse
from .middleware import *
from django.utils.decorators import decorator_from_middleware
from datetime import datetime
from .services import *
from django.core.paginator import Paginator


def allEmailHook(page):
    try:
        allEmailHook = AddEmailHooksModel.objects.all()
        paginator = Paginator(allEmailHook, 5)
        contacts = paginator.get_page(page)
        return contacts,contacts.paginator.page_range,None
    except Exception as e:
        logger.error(e)
        return None,None,e

def allemailtamps(page):
    try:
        allemailtamps = EmailTemplateModel.objects.all()
        paginator = Paginator(allemailtamps, 5)
        contacts = paginator.get_page(page)
        return contacts,contacts.paginator.page_range,None
    except Exception as e:
        logger.error(e)
        return None,None,e

def allMainEmailLayout(page):
    try:
        allmainemaillayout = MainEmailLayoutModel.objects.all()
        paginator = Paginator(allmainemaillayout, 5)
        contacts = paginator.get_page(page)
        return contacts,contacts.paginator.page_range,None
    except Exception as e:
        logger.error(e)
        return None, None, e


@decorator_from_middleware(EmailHookMiddleware)
def EmailHook(request, form, page=1):
    if request.method == "POST":
        try:
            CreateEmailhookService.execute({
                "title": form.cleaned_data.get("title"),
                "hook": form.cleaned_data.get("hook"),
                "description": form.cleaned_data.get("description"),
                "status": int(form.cleaned_data.get("status")),
                "userid": request.user,
            })
            lastid = AddEmailHooksModel.objects.last()
            logger.info(ugettext("New Email Hook Successfully Created at id {}".format(lastid.id)))
            return TemplateResponse(request, "adminapp/pages/mailbox/mailbox.html",{"emhook":"active","ificon": AdminInfo(request.user), "msg": ugettext("Successfully Created"),"range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":allEmailHook(page)[2]})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/mailbox/mailbox.html",{"emhook":"active","ificon": AdminInfo(request.user), "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":e if allEmailHook(page)[2] else e})

@decorator_from_middleware(AddEmailHookMiddleware)
def AddEmailHook(request, form,page=1):
    if request.method == "POST":
        try:
            CreateEmailhookService.execute({
                "title": form.cleaned_data.get("title"),
                "hook": form.cleaned_data.get("hook"),
                "description": form.cleaned_data.get("description"),
                "status": int(form.cleaned_data.get("status")),
                "userid": request.user,
            })
            lastid = AddEmailHooksModel.objects.last()
            logger.info(ugettext("New Email Hook Successfully Created at id {}".format(lastid.id)))
            return TemplateResponse(request,  "adminapp/pages/mailbox/addemailhook.html",  {"emhook":"active","ificon": AdminInfo(request.user), "msg":ugettext("Successfully Created"),"range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":allEmailHook(page)[2]})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/addemailhook.html",  {"emhook":"active","ificon": AdminInfo(request.user),  "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":e if allEmailHook(page)[2] else e})



@decorator_from_middleware(ViewEmailHookMiddleware)
def ViewEmailHook(request,id,page=1):
    try:
        viewhookemail = AddEmailHooksModel.objects.get(id=id)
        return TemplateResponse(request,  "adminapp/pages/mailbox/viewemailhook.html", {"emhook":"active","ificon": AdminInfo(request.user), "viewhookemail": viewhookemail})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/mailbox/mailbox.html",{"emhook": "active", "ificon": AdminInfo(request.user), "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":e if allEmailHook(page)[2] else e})


@decorator_from_middleware(ViewEmailHookMiddleware)
def DeleteEmailHook(request,id,page=1):
    try:
        viewhookemail = AddEmailHooksModel.objects.get(id=id)
        viewhookemail.delete()
        logger.info(ugettext("Email Hook id {} Successfully Deleted".format(id)))
        return TemplateResponse(request,  "adminapp/pages/mailbox/mailbox.html", {"emhook":"active","ificon": AdminInfo(request.user), "msg":ugettext("Successfully Deleted"), "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":allEmailHook(page)[2]})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/mailbox/mailbox.html",{"emhook": "active", "ificon": AdminInfo(request.user), "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":e if allEmailHook(page)[2] else e})


@decorator_from_middleware(EditEmailHookMiddleware)
def EditEmailHook(request, form, id,page=1):
    if request.method == "POST":
        try:
            UpdateEmailhookService.execute({
                "title": form.cleaned_data.get("title"),
                "hook": form.cleaned_data.get("hook"),
                "description": form.cleaned_data.get("description"),
                "status": int(form.cleaned_data.get("status")),
                "id": id,
            })
            logger.info(ugettext("Email Hook Id {} Successfully Updated".format(id)))
            return TemplateResponse(request, "adminapp/pages/mailbox/editemailhook.html",{"emhook":"active", "viewhookemail":  AddEmailHooksModel.objects.get(id=id), "ificon": AdminInfo(request.user),"msg": ugettext("Successfully Updated"), "range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":allEmailHook(page)[2]})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request, "adminapp/pages/mailbox/editemailhook.html",{"emhook":"active","viewhookemail": AddEmailHooksModel.objects.get(id=id), "ificon": AdminInfo(request.user),"range":allEmailHook(page)[1],"allemailhook": allEmailHook(page)[0],"error":e if allEmailHook(page)[2] else e})


@decorator_from_middleware(MainEmailLayoutViewMiddleware)
def MainEmailLayoutView(request,id):
    try:
        tempemaildata = MainEmailLayoutModel.objects.get(id=id)
        return TemplateResponse(request,  "adminapp/pages/mailbox/mainemaillayout.html",{"emtemp":"active","listmel": tempemaildata, "ificon": AdminInfo(request.user), "emailtamps": EmailTemplateModel.objects.all()})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request,  "adminapp/pages/mailbox/mainemaillayout.html",{"emtemp":"active","error": e, "ificon": AdminInfo(request.user), "emailtamps": EmailTemplateModel.objects.all()})




def ListMainEmailLayoutView(request,page=1):
    return render(request,  "adminapp/pages/mailbox/listmainemaillayout.html", {"emtemp":"active","listmel": allMainEmailLayout(page)[0],"range":allMainEmailLayout(page)[1],"error":allMainEmailLayout(page)[2], "ificon": AdminInfo(request.user)})



@decorator_from_middleware(AddMainEmailLayoutMiddleware)
def AddMainEmailLayoutView(request,form):
    if request.method == "POST":
        try:
            CreateMainEmailLayoutService.execute({
                "title": form.cleaned_data.get('title'),
                "layout_html": form.cleaned_data.get('layout_html'),
                "user": request.user
            })
            logger.info(ugettext("New Main Email Layout Successfully Added"))
            return TemplateResponse(request,  "adminapp/pages/mailbox/addmainemaillayout.html",  {"emtemp":"active","ificon": AdminInfo(request.user)})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/addmainemaillayout.html",  {"emtemp":"active","ificon": AdminInfo(request.user),"error":e})


@decorator_from_middleware(EditMainEmailLayoutMiddleware)
def EditMainEmailLayoutView(request,form,id):
    if request.method == "POST":
        try:
            EditMainEmailLayoutService.execute({
                "title": form.cleaned_data.get('title'),
                "layout_html": form.cleaned_data.get('layout_html'),
                "user": request.user,
                "id": id
            })
            logger.info(ugettext("Main Email Layout Id {} Successfully Updated".format(id)))
            return TemplateResponse(request,  "adminapp/pages/mailbox/editmainemaillayout.html",{"emtemp":"active","ificon": AdminInfo(request.user), "editemel":  MainEmailLayoutModel.objects.get(id=id), "msg": ugettext("Successfully Updated")})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/editmainemaillayout.html",{"emtemp":"active","ificon": AdminInfo(request.user), "editemel":  MainEmailLayoutModel.objects.get(id=id),  "error":  e})

@decorator_from_middleware(MainEmailLayoutViewMiddleware)
def DeleteMainEmailLayoutView(request, id,page=1):
    try:
        editemel = MainEmailLayoutModel.objects.get(id=request.GET[id])
        editemel.delete()
        logger.info(ugettext("Main Email Layout Id {} Successfully Deleted".format(id)))
        return TemplateResponse(request,  "adminapp/pages/mailbox/listmainemaillayout.html", {"emtemp":"active", "listmel": allMainEmailLayout(page)[0],"range":allMainEmailLayout(page)[1],"error":allMainEmailLayout(page)[2], "ificon": AdminInfo(request.user), "msg": ugettext("Successfully Deleted")})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request,  "adminapp/pages/mailbox/listmainemaillayout.html", {"emtemp":"active", "listmel": allMainEmailLayout(page)[0],"range":allMainEmailLayout(page)[1],"error":e if allMainEmailLayout(page)[2] else e, "ificon": AdminInfo(request.user)})





@decorator_from_middleware(EmailTemplateMiddleware)
def EmailTemplateView(request,form,page=1):
    if request.method == "POST":
        try:
            CreateEmailTemplateService.execute({
                "emailhooks": form.cleaned_data.get("emailhooks"),
                "subject": form.cleaned_data.get("subject"),
                "ckeditor": form.cleaned_data.get("ckeditor"),
                "footer_text": form.cleaned_data.get("footer_text"),
                "email_preference": form.cleaned_data.get("email_preference"),
                "status": int(form.cleaned_data.get("status")),
                "user": request.user,
            })
            lastid = EmailTemplateModel.objects.last()
            logger.info(ugettext("New Email Template Id {} Successfully Added".format(lastid.id)))
            return TemplateResponse(request,  "adminapp/pages/mailbox/read-mail.html", {"emtemp": "active", "ificon": AdminInfo(request.user),  "msg":ugettext("Successfully Created"), "allemailhooks":  AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":allemailtamps(page)[2], "mellist": MainEmailLayoutModel.objects.get()})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/read-mail.html", {"emtemp":"active","error": e,  "ificon": AdminInfo(request.user), "allemailhooks":  AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":allemailtamps(page)[2], "mellist": MainEmailLayoutModel.objects.get()})



@decorator_from_middleware(AddEmailTemplateMiddleware)
def AddEmailTemplateView(request,form,page=1):
    if request.method == "POST":
        try:
            CreateEmailTemplateService.execute({
                "emailhooks": form.cleaned_data.get("emailhooks"),
                "subject": form.cleaned_data.get("subject"),
                "ckeditor": form.cleaned_data.get("ckeditor"),
                "footer_text": form.cleaned_data.get("footer_text"),
                "email_preference": form.cleaned_data.get("email_preference"),
                "status": int(form.cleaned_data.get("status")),
                "user": request.user,
            })
            lastid = EmailTemplateModel.objects.last()
            logger.info(ugettext("New Email Template Id {} Successfully Added".format(lastid.id)))
            return TemplateResponse(request,  "adminapp/pages/mailbox/addemailtemplate.html", {"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user), "msg":ugettext("Successfully Created"), "allemailhooks":  AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":allemailtamps(page)[2]})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/addemailtemplate.html",  {"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(),  "ificon": AdminInfo(request.user), "allemailhooks": AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":e if allemailtamps(page)[2] else e})


@decorator_from_middleware(ViewEmailTemplateMiddleware)
def ViewEmailTemplateView(request,id,page=1):
    try:
        tempemaildata = EmailTemplateModel.objects.get(id=id)
        return TemplateResponse(request,  "adminapp/pages/mailbox/viewemailtemplate.html", {"emtemp":"active","ificon": AdminInfo(request.user), "emailtamps":  tempemaildata, "mellist": MainEmailLayoutModel.objects.get()})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/mailbox/read-mail.html",{"emtemp": "active",  "ificon": AdminInfo(request.user),"allemailhooks": AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":e if allemailtamps(page)[2] else e,"mellist": MainEmailLayoutModel.objects.get()})


@decorator_from_middleware(EditEmailTemplateMiddleware)
def EditEmailTemplateView(request,form, id,page=1):
    if request.method == "POST":
        try:
            EditEmailTemplateService.execute({
                "emailhooks": form.cleaned_data.get("emailhooks"),
                "subject": form.cleaned_data.get("subject"),
                "ckeditor": form.cleaned_data.get("ckeditor"),
                "footer_text": form.cleaned_data.get("footer_text"),
                "email_preference": form.cleaned_data.get("email_preference"),
                "status": int(form.cleaned_data.get("status")),
                "user": request.user,
                "id":id
            })
            logger.info(ugettext("Email Template id {} Successfully Updated".format(id)))
            return TemplateResponse(request,  "adminapp/pages/mailbox/editemailtemplate.html", { "emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user), "allemailhooks":  AddEmailHooksModel.objects.all(), "msg": ugettext("Successfully Updated"), "range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":allemailtamps(page)[2], "tempemaildata": EmailTemplateModel.objects.get(id=id)})
        except Exception as e:
            logger.error(e)
            return TemplateResponse(request,  "adminapp/pages/mailbox/editemailtemplate.html", {"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user),  "allemailhooks":  AddEmailHooksModel.objects.all(), "range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":e if allemailtamps(page)[2] else e, "tempemaildata": EmailTemplateModel.objects.get(id=id)})



@decorator_from_middleware(ViewEmailTemplateMiddleware)
def DeleteEmailTemplateView(request, id,page=1):
    try:
        tempemaildata = EmailTemplateModel.objects.get(id=id)
        tempemaildata.delete()
        return TemplateResponse(request,  "adminapp/pages/mailbox/read-mail.html", {"emtemp":"active","ificon": AdminInfo(request.user), "allemailhooks":  AddEmailHooksModel.objects.all(), "range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":allemailtamps(page)[2]})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/mailbox/read-mail.html",{"emtemp": "active", "ificon": AdminInfo(request.user),"allemailhooks": AddEmailHooksModel.objects.all(),"range":allemailtamps(page)[1], "emailtamps": allemailtamps(page)[0],"error":e if allemailtamps(page)[2] else e,"mellist": MainEmailLayoutModel.objects.get()})




from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from POC.admininfo import *
from .forms import *



class EmailHookMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = AddEmailHookForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/mailbox/mailbox.html",
                              {"emhook":"active","ificon": AdminInfo(request.user), "form": form,"allemailhook": AddEmailHooksModel.objects.all()})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/mailbox/mailbox.html", {"emhook":"active","ificon": AdminInfo(request.user), "allemailhook": AddEmailHooksModel.objects.all()})

    def process_template_response(self, request, response):
        return response


class AddEmailHookMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = AddEmailHookForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/mailbox/addemailhook.html",
                              {"emhook":"active","ificon": AdminInfo(request.user), "form": form,"allemailhook": AddEmailHooksModel.objects.all()})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/mailbox/addemailhook.html",
                      {"emhook":"active","ificon": AdminInfo(request.user),"allemailhook": AddEmailHooksModel.objects.all()})

    def process_template_response(self, request, response):
        return response


class ViewEmailHookMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" not in view_kwargs and not view_kwargs['id']:
            if not AddEmailHooksModel.objects.filter(id=view_kwargs['id']):
                logger.error(ugettext("Email Hook id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emhook":"active","ificon": AdminInfo(request.user)}, status= 404)
            logger.error(ugettext("Email Hook id {} not found".format(view_kwargs['id'])))
            return render(request, 'adminapp/pages/examples/404.html', {"emhook":"active","ificon": AdminInfo(request.user)}, status=404)
    def process_template_response(self, request, response):
        return response

class EditEmailHookMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" in view_kwargs and view_kwargs['id']:
            if AddEmailHooksModel.objects.filter(id=view_kwargs['id']):
                viewhookemail = AddEmailHooksModel.objects.get(id=view_kwargs['id'])
                if request.method == "POST":
                    form = AddEmailHookForm(request.POST)
                    if not form.is_valid():
                        logger.error(form.errors)
                        logger.error(form.non_field_errors)
                        return render(request, "adminapp/pages/mailbox/editemailhook.html",{"emhook":"active","ificon": AdminInfo(request.user), "viewhookemail": viewhookemail,"form": form})
                    else:
                        return view_func(request,form,view_kwargs['id'])
                return render(request, "adminapp/pages/mailbox/editemailhook.html",{"emhook":"active","ificon": AdminInfo(request.user), "viewhookemail": viewhookemail,"allemailhook": AddEmailHooksModel.objects.all()})
            else:
                logger.error(ugettext("Email Hook id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emhook":"active","ificon": AdminInfo(request.user)},status=404)
        else:
            logger.error(ugettext("Email Hook id {} not found".format(view_kwargs['id'])))
            return render(request, 'adminapp/pages/examples/404.html', {"emhook":"active","ificon": AdminInfo(request.user)}, status=404)

    def process_template_response(self, request, response):
        return response



class MainEmailLayoutViewMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" not in view_kwargs and not view_kwargs['id']:
            if not MainEmailLayoutModel.objects.filter(id=view_kwargs['id']):
                logger.error(ugettext("Main Email Layout id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)
            logger.error(ugettext("Main Email Layout id {} not found".format(view_kwargs['id'])))
            return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)}, status=404)

    def process_template_response(self, request, response):
        return response

class AddMainEmailLayoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = AddMainEmailLayoutForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/mailbox/addmainemaillayout.html",{"emtemp":"active","ificon": AdminInfo(request.user),"form":form})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/mailbox/addmainemaillayout.html",{"emtemp":"active","ificon": AdminInfo(request.user)})

    def process_template_response(self, request, response):
        return response


class EditMainEmailLayoutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" in view_kwargs and view_kwargs['id']:
            if MainEmailLayoutModel.objects.filter(id=view_kwargs['id']):
                editemel = MainEmailLayoutModel.objects.get(id=view_kwargs['id'])
                if request.method == "POST":
                    form = AddMainEmailLayoutForm(request.POST)
                    if not form.is_valid():
                        logger.error(form.errors)
                        logger.error(form.non_field_errors)
                        return render(request, "adminapp/pages/mailbox/editmainemaillayout.html",
                                      {"emtemp":"active","ificon": AdminInfo(request.user), "editemel": editemel,"form":form})
                    else:
                        return view_func(request,form,view_kwargs['id'])
                return render(request,  "adminapp/pages/mailbox/editmainemaillayout.html",  {"emtemp":"active","ificon": AdminInfo(request.user), "editemel": editemel})
            else:
                logger.error(ugettext("Main Email Layout id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)
        else:
            logger.error(ugettext("Main Email Layout id {} not found".format(view_kwargs['id'])))
            return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)}, status=404)
    def process_template_response(self, request, response):
        return response


class EmailTemplateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = EmailTemplateForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request,  "adminapp/pages/mailbox/read-mail.html", {"emtemp":"active","ificon": AdminInfo(request.user), "form":  form, "allemailhooks":  AddEmailHooksModel.objects.all(), "emailtamps": EmailTemplateModel.objects.all(), "mellist": MainEmailLayoutModel.objects.get()})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/mailbox/read-mail.html",{"emtemp":"active","ificon": AdminInfo(request.user),"allemailhooks": AddEmailHooksModel.objects.all(),"emailtamps": EmailTemplateModel.objects.all(), "mellist": MainEmailLayoutModel.objects.get()})

    def process_template_response(self, request, response):
        return response


class AddEmailTemplateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = EmailTemplateForm(request.POST)
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request,  "adminapp/pages/mailbox/addemailtemplate.html", {"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user),  "form": form, "allemailhooks":  AddEmailHooksModel.objects.all(), "emailtamps": EmailTemplateModel.objects.all()})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/mailbox/addemailtemplate.html",{"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user),"allemailhooks": AddEmailHooksModel.objects.all(),"emailtamps": EmailTemplateModel.objects.all()})

    def process_template_response(self, request, response):
        return response



class ViewEmailTemplateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" not in view_kwargs and not view_kwargs['id']:
            if not EmailTemplateModel.objects.filter(id=view_kwargs['id']):
                logger.error(ugettext("Email Template id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)
            logger.error(ugettext("Email Template id {} not found".format(view_kwargs['id'])))
            return render(request,  'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)

    def process_template_response(self, request, response):
        return response


class EditEmailTemplateMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "id" in view_kwargs and view_kwargs['id']:
            if EmailTemplateModel.objects.filter(id=view_kwargs['id']):
                tempemaildata = EmailTemplateModel.objects.get(id=view_kwargs['id'])
                if request.method == "POST":
                    form = EmailTemplateForm(request.POST)
                    if not form.is_valid():
                        logger.error(form.errors)
                        logger.error(form.non_field_errors)
                        return render(request,  "adminapp/pages/mailbox/editemailtemplate.html", {"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user),  "allemailhooks":  AddEmailHooksModel.objects.all(), "form": form, "emailtamps":  EmailTemplateModel.objects.all(), "tempemaildata": tempemaildata})
                    else:
                        return view_func(request,form,view_kwargs['id'])
                return render(request, "adminapp/pages/mailbox/editemailtemplate.html",{"emtemp":"active","mellist": MainEmailLayoutModel.objects.get(), "ificon": AdminInfo(request.user),"allemailhooks": AddEmailHooksModel.objects.all(),"emailtamps": EmailTemplateModel.objects.all(), "tempemaildata": tempemaildata})
            else:
                logger.error(ugettext("Email Template id {} not found".format(view_kwargs['id'])))
                return render(request, 'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)
        else:
            logger.error(ugettext("Email Template id {} not found".format(view_kwargs['id'])))
            return render(request,  'adminapp/pages/examples/404.html', {"emtemp":"active","ificon": AdminInfo(request.user)},status=404)

    def process_template_response(self, request, response):
        return response
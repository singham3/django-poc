from POC.admininfo import *
from .models import *
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from .forms import *

class AllCMSPagesMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response

class DeleteCMSPagesMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' not in view_kwargs and not view_kwargs['id']:
            logger.error("CMS Page id {} not found".format(view_kwargs['id']))
            return render(request, 'adminapp/pages/examples/404.html', {"cms":"active","ificon": AdminInfo(request.user)}, status=404)
        else:
            if not CMSpagemodel.objects.filter(id=view_kwargs['id']).exists():
                logger.error("CMS Page id {} not found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"cms":"active","ificon": AdminInfo(request.user)},status=404)
            return None

class EditCMSPagesMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' in view_kwargs and view_kwargs['id']:
            if CMSpagemodel.objects.filter(id=view_kwargs['id']).exists():
                cmsdata = CMSpagemodel.objects.get(id=view_kwargs['id'])
                if request.method == "POST":
                    form = CMSpageform(request.POST,request.FILES)
                    if not form.is_valid():
                        logger.error(form.errors)
                        logger.error(form.non_field_errors)
                        return render(request, "adminapp/pages/forms/editeditors.html",{"cms":"active","ificon": AdminInfo(request.user), "cmsdata": cmsdata, "from":form}, status=500)
                    else:
                        return view_func(request,form,view_kwargs['id'])
                return render(request, "adminapp/pages/forms/editeditors.html",{"cms":"active","ificon": AdminInfo(request.user), "cmsdata": cmsdata})
            else:
                logger.error("CMS Page id {} not found".format(view_kwargs['id']))
                return render(request, 'adminapp/pages/examples/404.html', {"cms":"active","ificon": AdminInfo(request.user)},status=404)
        else:
            logger.error("CMS Page  id not found in URL")
            return render(request, 'adminapp/pages/examples/404.html', {"cms":"active","ificon": AdminInfo(request.user)},status=404)

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            return response


class AddCMSPagesMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = CMSpageform(request.POST,request.FILES)
            if "cmsfile" not in request.FILES:
                logger.error("CMS New Page Add has File Feild is required")
                return render(request, "adminapp/pages/forms/editors.html",
                              {"cmd": "active","error": "File Field is required", "ificon": AdminInfo(request.user)})
            if not form.is_valid():
                logger.error(form.errors)
                logger.error(form.non_field_errors)
                return render(request, "adminapp/pages/forms/editors.html",{"cms": "active", "form": form,"ificon": AdminInfo(request.user)})
            else:
                return view_func(request,form)
        return render(request, "adminapp/pages/forms/editors.html", {"cms": "active", "ificon": AdminInfo(request.user)})

from django.shortcuts import render
from .models import *
from POC.admininfo import *
from datetime import datetime
from django.utils.decorators import decorator_from_middleware
from django.template.response import TemplateResponse
from .middleware import *
from .services import *
from django.utils import translation
from django.core.paginator import Paginator
from wsgiref.util import FileWrapper
import mimetypes
import sys
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView

def cmsdata(page):
    try:
        cmsdata = CMSpagemodel.objects.all()
        paginator = Paginator(cmsdata, 10)
        contacts = paginator.get_page(page)
        return contacts,contacts.paginator.page_range,None
    except Exception as e:
        logger.error(e)
        return None,None,e


@decorator_from_middleware(AllCMSPagesMiddleware)
def CMSPages(request, page=1):
    return render(request, "adminapp/pages/tables/cmspagestables.html", {"cms": "active","ificon": AdminInfo(request.user),"range":cmsdata(page)[1], "cmsdata": cmsdata(page)[0],"error":cmsdata(page)[2]})



@decorator_from_middleware(DeleteCMSPagesMiddleware)
def DeleteCMSPages(request, id,page=1):
    try:
        delcmsdata = CMSpagemodel.objects.get(id=id)
        delcmsdata.delete()
        logger.info("CMS page id {} Successfully Deleted".format(id))
        return TemplateResponse(request, "adminapp/pages/tables/cmspagestables.html",
                                {"cms": "active", "ificon": AdminInfo(request.user),
                                 "range":cmsdata(page)[1], "cmsdata": cmsdata(page)[0],"error":cmsdata(page)[2],"msg": ugettext("Successfully Deleted")})

    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/tables/cmspagestables.html",
                                {"cms": "active", "ificon": AdminInfo(request.user),"range":cmsdata(page)[1], "cmsdata": cmsdata(page)[0],"error": e if cmsdata(page)[2] else e})


@decorator_from_middleware(DeleteCMSPagesMiddleware)
def ViewCMSPages(request,id,page=1):
    try:
        viewcmsdata = CMSpagemodel.objects.get(id=id)
        return TemplateResponse(request, "adminapp/pages/examples/cmdpageview.html",{"cms":"active","ificon": AdminInfo(request.user), "cmsdata": viewcmsdata})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        errors = str((e, exc_type, fname, exc_tb.tb_lineno))
        logger.error(str((e, exc_type, fname, exc_tb.tb_lineno)))
        return TemplateResponse(request, "adminapp/pages/tables/cmspagestables.html",{"cms": "active", "ificon": AdminInfo(request.user), "range":cmsdata(page)[1], "cmsdata": cmsdata(page)[0],"error":errors if cmsdata(page)[2] else errors})


@decorator_from_middleware(DeleteCMSPagesMiddleware)
def DownloadimagelinkView(request,id,page=1):
    try:
        viewcmsdata = CMSpagemodel.objects.get(id=id)
        wrapper = FileWrapper(viewcmsdata.cmsfile.file)
        filename = str(viewcmsdata.cmsfile.file).split('/')[-1]
        content_type = mimetypes.guess_type(str(viewcmsdata.cmsfile.file))[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        errors = str((e, exc_type, fname, exc_tb.tb_lineno))
        logger.error(str((e, exc_type, fname, exc_tb.tb_lineno)))
        return TemplateResponse(request, "adminapp/pages/tables/cmspagestables.html",{"cms": "active", "ificon": AdminInfo(request.user), "range":cmsdata(page)[1], "cmsdata": cmsdata(page)[0],"error":errors if cmsdata(page)[2] else errors})


@decorator_from_middleware(EditCMSPagesMiddleware)
def EditCMSPages(request, form, id):
    try:
        if request.method == "POST":
            EditCMSPageService.execute({
                "id": id,
                "title": form.cleaned_data.get('title'),
                "meta_title": form.cleaned_data.get('meta_title'),
                'sub_title': form.cleaned_data.get('sub_title'),
                "meta_keyword": form.cleaned_data.get('meta_keyword'),
                "slug": form.cleaned_data.get('slug'),
                "meta_description": form.cleaned_data.get('meta_description'),
                "short_description": form.cleaned_data.get('short_description'),
                "cktextarea": form.cleaned_data.get('cktextarea')
            }, {"cmsfile": form.cleaned_data.get('cmsfile')})
            logger.info("CMS Page Id {} Successfully Updated".format(id))
            return TemplateResponse(request, "adminapp/pages/forms/editeditors.html",{"cms":"active","cmsdata": CMSpagemodel.objects.get(id=id), "msg":ugettext("Successfully Updated")})
    except Exception as e:
        logger.error(e)
        return TemplateResponse(request, "adminapp/pages/forms/editeditors.html",{"cms":"active","ificon": AdminInfo(request.user), "cmsdata": CMSpagemodel.objects.get(id=id), "error": e}, status=500)


@decorator_from_middleware(AddCMSPagesMiddleware)
def AddCMSPages(request, form):
    try:
        if request.method == "POST":
            CreateCMSPageService.execute({
                "title": form.cleaned_data.get('title'),
                "meta_title": form.cleaned_data.get('meta_title'),
                "sub_title": form.cleaned_data.get('sub_title'),
                "meta_keyword": form.cleaned_data.get('meta_keyword'),
                "slug": form.cleaned_data.get('slug'),
                "meta_description": form.cleaned_data.get('meta_description'),
                "short_description": form.cleaned_data.get('short_description'),
                "cktextarea": form.cleaned_data.get('cktextarea'),
                "userid": request.user
            }, {"cmsfile": form.cleaned_data.get('cmsfile')})
            lastid = CMSpagemodel.objects.last()
            logger.info("CMS Page New Id {} Successfully Added".format(lastid.id))
            return render(request, "adminapp/pages/forms/editors.html",{"cms":"active","ificon": AdminInfo(request.user), "msg": ugettext("Successfully Updated")})
    except Exception as e:
        logger.error(e)
        return render(request, "adminapp/pages/forms/editors.html",{"cms": "active", "error": e, "ificon": AdminInfo(request.user)})





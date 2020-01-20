"""POC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from rest_framework import routers
from django.conf import settings
from Django_Dynamic_Models.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from adminapp.views import *
from settings.views import *
from CMSpages.views import *
from email_templates.views import *
from django.conf.urls import url
from django.urls import path,include
from django.conf.urls.static import static
from django.views.static import serve


router = routers.DefaultRouter()

urlpatterns = [
    path('dashboard/', Home),
    path('', Login),
    path('login/', Login),
    path('logout/', LogotView),
    path('adminuser/forgot/', ForgetPassword),
    path('adminuser/forgot/referral/', Verifyforgetpass),
    path('user/profile/', Profile),
    path('users/pages/<int:page>/', Usertable),
    path('users/pages/', Usertable),
    path('admin/', admin.site.urls),
    path('users/pages/add/', Adduser),
    path('users/pages/view/<int:id>/', Viewuser),
    path('users/pages/edit/<int:id>/', Edituserdata),
    path('users/pages/delete/<int:id>/', Deleteuser),
    path('cms-manager/pages/<int:page>/', CMSPages),
    path('cms-manager/pages/', CMSPages),
    path('cms-manager/pages/add/', AddCMSPages),
    path('cms-manager/pages/view/<int:id>/', ViewCMSPages),
    path('cms-manager/pages/view/image/<int:id>/', DownloadimagelinkView),
    path('cms-manager/pages/edit/<int:id>/', EditCMSPages),
    path('cms-manager/pages/delete/<int:id>/', DeleteCMSPages),
    path('email-manager/email-hooks/', EmailHook),
    path('email-manager/email-hooks/<int:page>/', EmailHook),
    path('email-manager/email-hooks/add/', AddEmailHook),
    path('email-manager/email-hooks/add/<int:page>/', AddEmailHook),
    path('email-manager/email-hooks/view/<int:id>/', ViewEmailHook),
    path('email-manager/email-hooks/edit/<int:id>/', EditEmailHook),
    path('email-manager/email-hooks/edit/<int:id>/<int:page>/', EditEmailHook),
    path('email-manager/email-hooks/delete/<int:id>/', DeleteEmailHook),
    path('email-manager/email-templates/', EmailTemplateView),
    path('email-manager/email-templates/<int:page>/', EmailTemplateView),
    path('email-manager/email-templates/add/', AddEmailTemplateView),
    path('email-manager/email-templates/add/<int:page>/', AddEmailTemplateView),
    path('email-manager/email-templates/edit/<int:id>/', EditEmailTemplateView),
    path('email-manager/email-templates/edit/<int:id>/<int:page>/', EditEmailTemplateView),
    path('email-manager/email-templates/delete/<int:id>/', DeleteEmailTemplateView),
    path('email-manager/email-templates/view/<int:id>/', ViewEmailTemplateView),
    path('email-template/email-preferences/', ListMainEmailLayoutView),
    path('email-template/email-preferences/<int:page>/', ListMainEmailLayoutView),
    path('email-template/email-preferences/view/<int:id>/', MainEmailLayoutView),
    path('email-template/email-preferences/add/', AddMainEmailLayoutView),
    path('email-template/email-preferences/edit/<int:id>/', EditMainEmailLayoutView),
    path('email-template/email-preferences/delete/<int:id>/', DeleteMainEmailLayoutView),
    path("setting-manager/settings/social/", Addsociallins),
    path("setting-manager/settings/social/<int:page>/", Addsociallins),
    path("setting-manager/settings/social/delete/", Deletesociallins.as_view(), name="Deletesociallins"),
    path("setting-manager/settings/smtp/", SMTPdeatils),
    path('setting-manager/settings/', Generalform),
    path('setting-manager/settings/<int:page>/', Generalform),
    path("setting-manager/settings/add/", AddGeneralsetting),
    path("setting-manager/settings/view/<int:id>/", ViewGeneralSettings),
    path("setting-manager/settings/edit/<int:id>/", Editgeneralsettings),
    path("setting-manager/settings/logos/", AddLogoFavicon),
    path("setting-manager/settings/logos/<int:page>/", AddLogoFavicon),
    path("setting-manager/settings/logos/delete/", LogoFavDelete.as_view(), name="LogoFavDelete"),
    path("Dynamic-Model/create-model/", CreateDynamicModelView),
    path("api/v1/model/test/", DynamicModelView.as_view(), name="DynamicModel")
]


if not settings.DEBUG:
    urlpatterns += [
                    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                    ]

handler404 = 'adminapp.views.view_404'
handler500 = 'adminapp.views.view_500'

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

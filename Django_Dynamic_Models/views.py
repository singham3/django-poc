from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db import models
from django.core.management import call_command
from .models import *


class DynamicModelView(APIView):
    def post(self, request):
        attrs = {
            'name': models.CharField(max_length=32),
            '__module__': 'Django_Dynamic_Models.models'
        }
        Animal = type("Animal", (models.Model,), attrs)

        call_command('makemigrations')
        call_command('migrate')
        print("Animal ---------- ",Animal)
        return HttpResponse("Hello World!")


def CreateDynamicModelView(request):
    if request.method == "POST":
        try:
            requestdata = dict(request.POST)
            requestdata.pop("csrfmiddlewaretoken")
            attrs = {
                '__module__': 'Django_Dynamic_Models.models'
            }
            flag = False
            for v in ["text","image","file","textarea","date","radio","checkbox"]:
                if v in requestdata:
                    flag = True
            model_class = """"""
            if flag:
                title = requestdata["title"]
                model_class = model_class+"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nclass {}(models.Model):\n\t""".format(title[0].replace(" ","_",title[0].count(" "))+"_Model")
                description = requestdata["description"]
                if "text" in request.POST:
                    text = list(set(requestdata['text']))
                    if len(text) == 1:
                        model_class = model_class+"{} = models.CharField(max_length=250)\n\t".format(text[0].replace(" ","_",text[0].count(" ")))
                        attrs.update({text[0].replace(" ","_",text[0].count(" ")): models.CharField(max_length=250)})
                    else:
                        for i in text:
                            model_class = model_class + "{} = models.CharField(max_length=250)\n\t".format(i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.CharField(max_length=250)})
                if "image" in request.POST:
                    image = list(set(requestdata["image"]))
                    if len(image) == 1:
                        model_class = model_class + "{} = models.ImageField(upload_to='{}/')\n\t".format(image[0].replace(" ","_",image[0].count(" ")),image[0].replace(" ","_",image[0].count(" ")))
                        attrs.update({image[0].replace(" ","_",image[0].count(" ")): models.ImageField(upload_to="{}/".join(image[0].replace(" ","_",image[0].count(" "))))})
                    else:
                        for i in image:
                            model_class = model_class+"{} = models.ImageField(upload_to='{}/')\n\t".format(i.replace(" ","_",i.count(" ")),i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.ImageField(upload_to="{}/".join(i.replace(" ","_",i.count(" "))))})
                if "file" in request.POST:
                    file = list(set(requestdata["file"]))
                    if len(file) == 1:
                        model_class = model_class + "{} = models.FileField(upload_to='{}/')\n\t".format(file[0].replace(" ","_",file[0].count(" ")),file[0].replace(" ","_",file[0].count(" ")))
                        attrs.update({file[0].replace(" ","_",file[0].count(" ")): models.FileField(upload_to="{}/".join(file[0].replace(" ","_",file[0].count(" "))))})
                    else:
                        for i in file:
                            model_class = model_class+"{} = models.FileField(upload_to='{}/')\n\t".format(i.replace(" ","_",i.count(" ")),i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.FileField(upload_to="{}/".join(i.replace(" ","_",i.count(" "))))})
                if "textarea" in request.POST:
                    textarea = list(set(requestdata["textarea"]))
                    if len(textarea) == 1:
                        model_class = model_class + "{} = models.TextField(max_length=5000)\n\t".format(textarea[0].replace(" ","_",textarea[0].count(" ")))
                        attrs.update({textarea[0].replace(" ","_",textarea[0].count(" ")): models.TextField(max_length=5000)})
                    else:
                        for i in textarea:
                            model_class = model_class+"{} = models.TextField(max_length=5000)\n\t".format(i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.TextField(max_length=5000)})
                if "date" in request.POST:
                    date = list(set(requestdata["date"]))
                    if len(date) == 1:
                        model_class = model_class+"{} = models.DateTimeField(auto_now_add=True)\n\t".format(date[0].replace(" ","_",date[0].count(" ")))
                        attrs.update({date[0].replace(" ","_",date[0].count(" ")): models.DateTimeField(auto_now_add=True)})
                    else:
                        for i in date:
                            model_class = model_class+"{} = models.DateTimeField(auto_now_add=True)\n\t".format(i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.DateTimeField(auto_now_add=True)})
                if "radio" in request.POST:
                    radio = list(set(requestdata["radio"]))
                    if len(radio) == 1:
                        model_class = model_class + "{} = models.BooleanField(default=False)\n\t".format(radio[0].replace(" ","_",radio[0].count(" ")))
                        attrs.update({radio[0].replace(" ","_",radio[0].count(" ")): models.BooleanField(default=False)})
                    else:
                        for i in radio:
                            model_class = model_class+ "{} = models.BooleanField(default=False)\n\t".format(i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.BooleanField(default=False)})
                if "checkbox" in request.POST:
                    checkbox = list(set(requestdata["checkbox"]))
                    if len(checkbox) == 1:
                        model_class = model_class + "{} = models.BooleanField(default=False)\n\t".format(checkbox[0].replace(" ","_",checkbox[0].count(" ")))
                        attrs.update({checkbox[0].replace(" ","_",checkbox[0].count(" ")): models.BooleanField(default=False)})
                    else:
                        for i in checkbox:
                            model_class = model_class + "{} = models.BooleanField(default=False)\n\t".format(i.replace(" ","_",i.count(" ")))
                            attrs.update({i.replace(" ","_",i.count(" ")): models.BooleanField(default=False)})
                print("\n\n\n")
                print(model_class)

                # requestdata.pop("description")
                # requestdata.pop("title")
                # dmdb = DynamicModulesModel(moduletitle=title[0],modulefiels=requestdata,moduledescription=description[0],userid=User.objects.get(username=request.user))
                # dmdb.save()
                # DynamicModule = type(title[0].replace(" ","_",title[0].count(" "))+"_Model", (models.Model,), attrs)
                #
                # call_command('makemigrations')
                # call_command('migrate')
                return render(request, "adminapp/pages/layout/dynamicmodel.html", {"msg": "Successfully Created"})
            else:
                return render(request, "adminapp/pages/layout/dynamicmodel.html", {"error": "No Field Found Please Select Any Field For New Module"})
        except Exception as e:
            print("error -- ",e)
            return render(request, "adminapp/pages/layout/dynamicmodel.html",{"error":e})

    return render(request, "adminapp/pages/layout/dynamicmodel.html")

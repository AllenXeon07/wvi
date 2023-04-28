from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views import generic
import pandas as pd
import os

# Create your views here.

class ChildRecordView():
    def view(request):
        template_name = "child_record.html"
        context = {
            "child_records" : ChildRecord.objects.all(),
            "kaders" : Kader.objects.all()
        }
        return render(request, template_name, context)
    
    def insert_excel(request):
        if request.method == "POST":
            template_name = "child_record.html"
            context = {"error" : "",
                        "child_records" : ChildRecord.objects.all(),
                         "kaders" : Kader.objects.all()
                        }
            file = request.FILES['file_excel']
            print(file.name)
            if(not('.xlsx' in file.name or '.csv' in file.name)):
                context ['error'] = "file type not correct" 
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                datas = pd.read_excel(filename)
                os.remove(filename)
                column_list = list(datas)

                important_column = [
                    'Child ID', 'Child Name', 'Gender',
                    'Project Number and Name', 'Community',
                    'RC Status', 'Age'
                ]
                
                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    ChildRecord.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'Child ID']
                        name = datas.loc[i, 'Child Name']
                        gender = datas.loc[i,'Gender']
                        community = datas.loc[i, 'Community']
                        age = datas.loc[i, 'Age']
                        project_number = datas.loc[i,'Project Number and Name']
                        status = datas.loc[i, 'RC Status']

                        child = Child.objects.get(pk=id)
                        if(child):
                            child.name = name
                            child.gender = gender
                            child.community = community
                            child.age = age
                            child.save()
                        else:
                            child = Child(id=id, name=name, gender=gender, community=community, age=age)
                            child.save()
                        childrecord = ChildRecord(child_id = child, project_number = project_number, status=status)
                        childrecord.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("childrecord"))
            else:
                return render(request, template_name, context)
        else:
            return ChildRecordView.view(request)

    def update(request):
        if request.method == "POST":
            id = request.POST['childrecord_id']
            kader_id = request.POST['kader_id']
            childrecord = ChildRecord.objects.get(pk=id) 
            if(kader_id != 'NULL'):
                kader = Kader.objects.get(pk=kader_id)
                childrecord.kader_id = kader
            else:
                childrecord.kader_id = None
            childrecord.save()
            return HttpResponseRedirect(reverse("childrecord"))
        else:
            return ChildRecordView.view(request) 


class KaderView():
    def view(request):
        template_name = "kader.html"
        context = {
            "kaders" : Kader.objects.all()
        }
        return render(request, template_name, context)
    
    def insert(request):
        if request.method == "POST":
            name = request.POST['name']
            number = request.POST['number']

            kader=  Kader(name=name, phone_number=number)
            kader.save()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)
    
    def update(request):
        if request.method == "POST":
            id = request.POST['kader_id']
            name = request.POST['name']
            number = request.POST['number']

            kader = Kader.objects.get(pk=id)
            kader.name = name
            kader.phone_number = number
            kader.save()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)

    def delete(request):
        if request.method == "POST":
            id = request.POST['kader_id']
           
            Kader.objects.get(pk=id).delete()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)


def index(request):
    childs = Child.objects.all()
    context = {
         "childs": childs
    }
    return render(request, "index.html", context)

def insert(request):
    id = request.POST['id']
    name = request.POST['name']
    community = request.POST['community']
    age = request.POST['age']

    child = Child(id=id, name=name, community=community, age=age)
    child.save()
    return HttpResponseRedirect(reverse("index"))

def insert_excel(request):
    file = request.FILES['file_excel']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)

    datas = pd.read_excel(filename)

    for i in range(len(datas)):
        id = datas.loc[i,'Child ID']
        name = datas.loc[i, 'Child Name']
        community = datas.loc[i, 'Community']
        age = datas.loc[i, 'Age']
        child = Child(id=id, name=name, community=community, age=age)
        child.save()
    
    os.remove(filename)
    return HttpResponseRedirect(reverse("index"))



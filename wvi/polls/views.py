from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views import generic
import pandas as pd
import datetime
import os

# Create your views here.

class ChildRecordView():
    def view(request):
        template_name = "child_record.html"
        context = {
            "child_records" : ChildRecord.objects.all(),
            "kaders" : Kader.objects.all(),
            "count_avail":  ChildRecord.objects.filter(status="1 - Available").count() ,
            "count_sponsored": ChildRecord.objects.filter(status="2 - Sponsored").count(),
            "count_hold": ChildRecord.objects.filter(status="3 - Hold").count(),
            "count_left":ChildRecord.objects.filter(status="4 - Left Program").count(),
            "param": Parameters.objects.get(pk=1).target_child
        }
        return render(request, template_name, context)
    
    def insert_excel(request):
        if request.method == "POST":
            template_name = "child_record.html"
            context = {"error" : "",
                        "child_records" : ChildRecord.objects.all(),
                         "kaders" : Kader.objects.all(),
            "count_avail":  ChildRecord.objects.filter(status="1 - Available").count() ,
            "count_sponsored": ChildRecord.objects.filter(status="2 - Sponsored").count(),
            "count_hold": ChildRecord.objects.filter(status="3 - Hold").count(),
            "count_left":ChildRecord.objects.filter(status="4 - Left Program").count(),
            "param": Parameters.objects.get(pk=1).target_child
                        }
            file = request.FILES['file_excel']
            if(not('.xlsx' in file.name or '.csv' in file.name)):
                context ['error'] = "file type incorrect" 
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

                        if(Child.objects.filter(pk=id).exists()):
                            child = Child.objects.get(pk=id)
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
        
    def update_target(request):
        if request.method == "POST": 
            target = request.POST['target']

            param = Parameters.objects.get(pk=1)
            param.target_child = target
            param.save()

            return HttpResponseRedirect(reverse("childrecord"))
        else:
            return ChildRecordView.view(request) 

class ChildView():
    def view(request):
        template_name = "index.html"
        context = {
            "childs": Child.objects.all()
        }
        return render(request, template_name, context)
    
    def update(request):
        if request.method == "POST":
            id = request.POST['child_id']
            rt = request.POST['rt']
            child = Child.objects.get(pk=id)
            child.rt = rt
            child.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return ChildView.view(request)

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

class CorrespondenceView():
    def view(request):
        template_name = "correspondence.html"
        for correspondence in Correspondence.objects.all():
            correspondence.days_before_due_date_field = (correspondence.due_date_field - datetime.datetime.now().date() ).days
            correspondence.days_before_due_date_system= (correspondence.due_date_system - datetime.datetime.now().date() ).days
            correspondence.save()
        context = {
            "correspondences" : Correspondence.objects.all(),
            "kaders" : Kader.objects.all(),
            "param" : Parameters.objects.get(pk=1).deadline_due_date_field
        }
        return render(request, template_name, context)
    
    def insert_excel(request):
        if request.method == "POST": 
            template_name = "correspondence.html"
            context = {
            "error" : "",
            "correspondences" : Correspondence.objects.all(),
            "kaders" : Kader.objects.all(),
            "param" : Parameters.objects.get(pk=1).deadline_due_date_field
            }

            file = request.FILES['file_excel']
            if(not('.xlsx' in file.name or '.csv' in file.name)):
                context ['error'] = "file type incorrect" 
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                datas = pd.read_excel(filename)
                os.remove(filename)
                column_list = list(datas)

                important_column = [
                    'Child ID', 'Child Name', 'Community',
                    'Correspondence Type', 'Creation Date',
                    'Mail Action and Route', 'Due Date Field',
                    'Due Date System', 'Days Before Due Date field',
                    'Days Before Due Date System', 'Status'
                ]

                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    Correspondence.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'Child ID']
                        name = datas.loc[i, 'Child Name']
                        community = datas.loc[i, 'Community']
                        type = datas.loc[i, 'Correspondence Type']
                        creation_date = datetime.datetime.strptime(datas.loc[i, 'Creation Date'], '%d-%b-%Y')
                        mail_action = datas.loc[i, 'Mail Action and Route']
                        due_date_field =  creation_date + datetime.timedelta(days=Parameters.objects.get(pk=1).deadline_due_date_field)
                        due_date_system = datetime.datetime.strptime(datas.loc[i, 'Due Date System'], '%d-%b-%Y')
                        days_before_due_date_field = (due_date_field - datetime.datetime.now() ).days
                        days_before_due_date_system = (due_date_system - datetime.datetime.now()).days
                        status = datas.loc[i, 'Status']

                        if(Child.objects.filter(pk=id).exists()):
                            child = Child.objects.get(pk=id)
                            child.name = name
                            child.community = community
                            child.save()
                        else:
                            child = Child(id=id, name=name, community=community)
                            child.save() 
                        correspondence = Correspondence(child_id = child, type = type, creation_date=creation_date, mail_action=mail_action, due_date_field=due_date_field, due_date_system=due_date_system, days_before_due_date_field=days_before_due_date_field, days_before_due_date_system=days_before_due_date_system, status=status)
                        correspondence.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("correspondence"))
            else:
                return render(request, template_name, context)
        else:
            return CorrespondenceView.view(request)

    def update_kader(request):
        if request.method == "POST":
            id = request.POST['correspondence_id']
            kader_id = request.POST['kader_id']
            corr = Correspondence.objects.get(pk=id) 
            if(kader_id != 'NULL'):
                kader = Kader.objects.get(pk=kader_id)
                corr.kader_id = kader
            else:
                corr.kader_id = None
            corr.save()
            return HttpResponseRedirect(reverse("correspondence"))
        else:
            return CorrespondenceView.view(request)

    def update_due_date(request):
        if request.method == "POST": 
            template_name = "correspondence.html"
            due_date = request.POST['due_date']

            param = Parameters.objects.get(pk=1)
            param.deadline_due_date_field = due_date
            param.save()

            for correspondence in Correspondence.objects.all():
                correspondence.due_date_field = correspondence.creation_date +  datetime.timedelta(days=Parameters.objects.get(pk=1).deadline_due_date_field)
                correspondence.save()
            return HttpResponseRedirect(reverse("correspondence"))
        else:
            return CorrespondenceView.view(request)

class ParticipantView():
    def view(request):
        template_name = "participant.html"
        context = {
            "participants" : Participation.objects.all()
        }
        return render(request, template_name, context)
    
    def insert_excel(request):
        if request.method == "POST":
            template_name = "child_record.html"
            context = {
                "error" : "",
                "participants" : Participation.objects.all()
            }
            file = request.FILES['file_excel']
            if(not('.xlsx' in file.name or '.csv' in file.name)):
                context ['error'] = "file type incorrect" 
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                datas = pd.read_excel(filename)
                os.remove(filename)
                column_list = list(datas)

                important_column = [
                    'Id', 'CommunityName',
                    'SdChildId', 'ChildName',
                    'Gender', 'AGE', 'ChildParticipation',
                    'FamilyParticipation', 'ChildSupport',
                    'FamilySupport', 'BenefitSupport'
                ]
                
                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    Participation.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'SdChildId']
                        name = datas.loc[i, 'ChildName']
                        gender = datas.loc[i,'Gender']
                        community = datas.loc[i, 'CommunityName']
                        age = datas.loc[i, 'AGE']
                        child_participation = datas.loc[i, 'ChildParticipation']
                        family_participation = datas.loc[i, 'FamilyParticipation']
                        child_support = datas.loc[i, 'ChildSupport']
                        family_support = datas.loc[i, 'FamilySupport']
                        benefit_support = datas.loc[i, 'BenefitSupport']


                        if(Child.objects.filter(pk=id).exists()):
                            child = Child.objects.get(pk=id)
                            child.name = name
                            child.gender = gender
                            child.community = community
                            child.age = age
                            child.save()
                        else:
                            child = Child(id=id, name=name, gender=gender, community=community, age=age)
                            child.save()
                        participation = Participation(child_id = child, child_participation = child_participation, family_participation = family_participation, child_support = child_support, family_support = family_support, benefit_support = benefit_support)
                        participation.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("childrecord"))
            else:
                return render(request, template_name, context)
        else:
            return ParticipantView.view(request)


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

def template(request):
    return render(request, "template.html")



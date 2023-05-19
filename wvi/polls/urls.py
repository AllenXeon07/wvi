from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("insert", views.insert, name='insert'),
    path("insert_excel", views.insert_excel, name="insert_excel"),

    path("child/update", views.ChildView.update),
   
    path("childrecord", views.ChildRecordView.view, name="childrecord"),
    path("childrecord/insert_excel", views.ChildRecordView.insert_excel),
    path("childrecord/update", views.ChildRecordView.update),
    path("childrecord/update_target", views.ChildRecordView.update_target),
    

    path("kader", views.KaderView.view, name="kader"),
    path("kader/insert", views.KaderView.insert),
    path("kader/update", views.KaderView.update),
    path("kader/delete", views.KaderView.delete),

    path("correspondence", views.CorrespondenceView.view, name="correspondence"),
    path("correspondence/insert_excel", views.CorrespondenceView.insert_excel),
    path("correspondence/update_kader", views.CorrespondenceView.update_kader),
    path("correspondence/update_due_date", views.CorrespondenceView.update_due_date),

    path("participant", views.ParticipantView.view, name="participant"),
    path("participant/insert_excel", views.ParticipantView.insert_excel, name="participant"),


    path("template", views.template, name="kader"),
    
    
    
]


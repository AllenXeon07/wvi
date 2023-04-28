from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("insert", views.insert, name='insert'),
    path("insert_excel", views.insert_excel, name="insert_excel"),

    path("childrecord", views.ChildRecordView.view, name="childrecord"),
    path("childrecord/insert_excel", views.ChildRecordView.insert_excel),
    path("childrecord/update", views.ChildRecordView.update),
    

    path("kader", views.KaderView.view, name="kader"),
    path("kader/insert", views.KaderView.insert),
    path("kader/update", views.KaderView.update),
    path("kader/delete", views.KaderView.delete),
    
]


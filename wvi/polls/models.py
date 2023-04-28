from django.db import models

# Create your models here.

class Child(models.Model):
    id = models.CharField(max_length = 20, primary_key=True)
    name = models.TextField(null=True)
    gender = models.CharField(max_length=7, null=True)
    community = models.TextField(null=True)
    age = models.CharField(max_length=4, null=True)

class Kader(models.Model):
    name = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, null=True)

class ChildRecord(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE)
    kader_id = models.ForeignKey(Kader, on_delete=models.CASCADE, null=True)
    project_number = models.TextField(null=True)
    status = models.TextField(null=True)

class Participation(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE)
    child_participation = models.IntegerField(null=True)
    family_participation = models.IntegerField(null=True)
    child_support = models.IntegerField(null=True)
    family_support = models.IntegerField(null=True)
    benefit_support = models.IntegerField(null=True)
    
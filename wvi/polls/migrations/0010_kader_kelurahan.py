# Generated by Django 4.1.7 on 2023-07-12 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_participation_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='kader',
            name='kelurahan',
            field=models.TextField(null=True),
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-13 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('H1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patients',
            old_name='DiseaseID',
            new_name='Disease',
        ),
    ]

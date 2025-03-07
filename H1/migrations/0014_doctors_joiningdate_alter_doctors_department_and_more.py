# Generated by Django 4.1.4 on 2023-01-17 09:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('H1', '0013_alter_patients_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='JoiningDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='Department',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='H1.department'),
        ),
        migrations.AlterField(
            model_name='patients',
            name='DOB',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

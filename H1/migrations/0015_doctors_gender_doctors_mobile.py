# Generated by Django 4.1.4 on 2023-01-17 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('H1', '0014_doctors_joiningdate_alter_doctors_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='Gender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='H1.gender'),
        ),
        migrations.AddField(
            model_name='doctors',
            name='Mobile',
            field=models.CharField(default=1111111111, max_length=10),
        ),
    ]

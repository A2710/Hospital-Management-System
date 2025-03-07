# Generated by Django 4.1.4 on 2023-01-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('H1', '0007_department_states_remove_patients_patientname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('GenderID', models.AutoField(primary_key=True, serialize=False)),
                ('GenderName', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RoomTypeID',
            fields=[
                ('RoomTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('RoomTypeName', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('SpecializationID', models.AutoField(primary_key=True, serialize=False)),
                ('SpecializationName', models.CharField(max_length=500)),
            ],
        ),
    ]

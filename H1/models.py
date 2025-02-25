from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Hospital(models.Model):
    HospitalID = models.AutoField(primary_key=True)
    HospitalName = models.CharField(max_length = 100)
    HospitalAddress = models.CharField(max_length = 1000)
    HospitalMobile = models.CharField(max_length=50)
    HospitalLandline = models.CharField(max_length=50)
    HospitalLogo = models.CharField(max_length=100)

class Diseases(models.Model):
    DiseaseID = models.AutoField(primary_key = True)
    DiseaseName = models.CharField(max_length=500)

class States(models.Model):
    StateID = models.AutoField(primary_key = True)
    StateName = models.CharField(max_length=500)

class Status(models.Model):
    StatusID = models.AutoField(primary_key = True)
    Status = models.CharField(max_length=500, default = "open")


class Department(models.Model):
    DepartmentID  = models.AutoField(primary_key = True)
    DepartmentName = models.CharField(max_length=500)

class Time(models.Model):
    TimeID = models.BigAutoField(primary_key=True)
    Time = models.TimeField(default = datetime.time)

class Gender(models.Model):
    GenderID  = models.AutoField(primary_key = True)
    GenderName = models.CharField(max_length=500)

class Specialization(models.Model):
    SpecializationID  = models.AutoField(primary_key = True)
    SpecializationName = models.CharField(max_length=500)

class RoomType(models.Model):
    RoomTypeID = models.AutoField(primary_key=True)
    RoomTypeName = models.CharField(max_length=500)

class Patients(models.Model):
    PatientID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=500, default = "NONE")
    MiddleName = models.CharField(max_length=500, default = "NONE")
    LastName = models.CharField(max_length=500, default = "NONE")
    Gender = models.ForeignKey(Gender, on_delete=models.CASCADE, default = 1)
    DOB = models.DateField(blank = False, default = timezone.now)
    Mobile = models.CharField(max_length=10, default = 1111111111)
    PatientAddress =  models.CharField(max_length=500)
    PatientImage = models.CharField(default = "", max_length=255)
    Email = models.EmailField(default = "abc@gmail.com")
    Consent = models.IntegerField(default = 0)
    ApprovalDate = models.DateField(blank = False, default = timezone.now)

class Doctors(models.Model):
    DoctorID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=500, default = "NONE")
    MiddleName = models.CharField(max_length=500, default = "NONE")
    LastName = models.CharField(max_length=500, default = "NONE")
    Gender = models.ForeignKey(Gender, default = 1, on_delete=models.CASCADE)
    JoiningDate = models.DateField(default= timezone.now)
    Mobile = models.CharField(max_length=10, default = 1111111111)
    DoctorAddress = models.CharField(max_length=500)
    Department = models.ForeignKey(Department,default=1, on_delete=models.CASCADE)
    Specialization = models.ForeignKey(Specialization,default=1, on_delete=models.CASCADE)
    DoctorImage = models.CharField(default = "", max_length=255)

class Medicines(models.Model):
    MedicineID = models.AutoField(primary_key=True)
    MedicineName = models.CharField(max_length=300)

class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Patient = models.ForeignKey(Patients, on_delete=models.PROTECT, default = 1)
    Department = models.ForeignKey(Department, on_delete=models.PROTECT, default = 1)
    Doctor = models.ForeignKey(Doctors, on_delete=models.PROTECT, default = 4)
    Time = models.ForeignKey(Time, on_delete=models.PROTECT, default = 1)
    AppointmentDate = models.DateField(default= timezone.now)
    Problem = models.CharField(max_length=5000)
    Status = models.CharField(default = "Active", max_length = 50)
    Prescription = models.CharField(default = "None", max_length = 5000)
    Report = models.CharField(default = "None", max_length=5000)

class deletedpatientapp(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Patient_F = models.CharField(max_length = 250, default = "None")
    Patient_M = models.CharField(max_length = 250, default = "None")
    Patient_L = models.CharField(max_length = 250, default = "None")
    Patient_Mo = models.CharField(max_length = 250, default = "None")
    Department = models.CharField(max_length = 250, default = "None")
    Doctor_F = models.CharField(max_length = 250, default = "None")
    Doctor_M = models.CharField(max_length = 250, default = "None")
    Doctor_L = models.CharField(max_length = 250, default = "None")
    Doctor_Mo = models.CharField(max_length = 250, default = "None")
    Time = models.TimeField()
    AppointmentDate = models.DateField()
    Problem = models.CharField(max_length=3000)
    Status = models.CharField(max_length = 50)
    Prescription = models.CharField(max_length = 4000)
    Report = models.CharField(max_length=3000)
    PatientImage = models.CharField(max_length=3000, default="/patient/no-photo.jpg")


class MenuMaster(models.Model):
    MenuID = models.AutoField(primary_key=True)
    ParentMenu = models.IntegerField(default = 0)
    MenuName = models.CharField(max_length = 200)
    MenuLink = models.CharField(max_length=200, default="link")
    MenuOrder = models.IntegerField(default = 0)
    HasSubmenu = models.IntegerField(default=1)

class HandleLogin(models.Model):
    LoginID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    UserPassword = models.CharField(max_length=50)
    superuser = models.IntegerField(default = 0)
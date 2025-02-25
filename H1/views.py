from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.template.loader import render_to_string
from H1.models import Patients,Medicines,Diseases,Department,Specialization,Gender,States,RoomType,Doctors,Time,Appointment,Hospital,HandleLogin
from django.db import connection
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import datetime
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import os
import pdfkit

# Create your views here.

def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def dictfetchall1(cursor1):
    desc = cursor1.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor1.fetchall()
    ]


@csrf_exempt

def index(request):
    session_user = request.session.get('userid','nouser')
    print(session_user)
    if (session_user == "nouser"):
        return HttpResponseRedirect("login")    

    return redirect('/sample')

#hospital

def hospital(request,id):

    showalert = 0
    if request.method == "POST":
        hospital_name = request.POST.get("hospitalname")
        hospital_address = request.POST.get("hospitaladdress")
        hospital_mobile = request.POST.get("hospitalmobile")
        hospital_landline = request.POST.get("hospitallandline")

        obj = Hospital(HospitalID = id, HospitalName = hospital_name, HospitalAddress = hospital_address, HospitalLandline = hospital_landline, HospitalMobile = hospital_mobile)
        obj.save()

        showalert = 1

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_hospital where HospitalID = " + str(id))
    h = dictfetchall(cursor)

    print(h)

    context = {"hospital":h,'showalert': showalert , 'pagetitle': "Hospital Details"}

    return render(request, "hospital.html", context)

def addpatient(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_diseases")
    r = dictfetchall(cursor)

    print(connection.queries)

    # context = {
    #     'omed': medicine,
    #     'count':count
    # }
    if request.method == "POST":
        
        name = request.POST.get('pname')
        address = request.POST.get('address')

        patient = Patients(PatientName = name, PatientAddress = address)
        patient.save()
        return redirect("/")

    return render(request, 'addpatient.html', {'data': r , 'pagetitle': "Add Patient"})





def editpatient(request,PatientID):

    if request.method == "POST":
        name = request.POST.get('pname')
        disease = request.POST.get('disease')
        address = request.POST.get('address')

        patient = Patients(PatientID = PatientID ,PatientName = name, Diseases_id = Diseases.objects.get(DiseaseName = disease), PatientAddress = address)
        patient.save()
        return HttpResponseRedirect("/")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_patients left outer join h1_diseases on h1_patients.Diseases_id = h1_diseases.DiseaseID where PatientID = " + str(PatientID))
        read = dictfetchall(cursor)
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM h1_diseases")
        dis = dictfetchall1(cursor1)
        print(read)
        #print(read.PatientID)
        #print(dis)
        print(connection.queries)
        
    return render(request, 'editpatient.html', {'p' : read, 'dis' : dis , 'pagetitle': "Edit Patient"})


def deletepatient(request,id):

    if request.method == 'POST':
        pi = Patients.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')


def medicines(request):

    medicine = Medicines.objects.all()
    count = Medicines.objects.all().count()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_medicines")
    r = dictfetchall(cursor)

    print(connection.queries)

    # context = {
    #     'omed': medicine,
    #     'count':count
    # }

    if request.method == "POST":
        return redirect("/")

    return render(request, 'medicines.html', {'data': r , 'pagetitle': "Medicine"})

#Login

def login(request):
    if(request.method=="POST"):
        
        username = request.POST.get("username")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_handlelogin where UserName = '" + username + "' and UserPassword = '" + password + "'")
        r = dictfetchall(cursor)

        print(len(r))

        if(len(r) > 0):
            request.session["userid"] = username
            request.session["superuser"] = r[0]['superuser']
            return HttpResponseRedirect("/sample")
        else:
            return render(request, 'login.html', {'error': "Username or Password does not match!"})            

    return render(request, 'login.html', {'error': "" , 'pagetitle': "Login"})

def logout(request):
    del request.session["userid"]
    return HttpResponseRedirect("/login")

def userlist(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_handlelogin")
    r = dictfetchall(cursor)

    return render(request, "user.html", {'pagetitle': "User List", "user": r})

def adduser(request):

    duplicate_error = 0

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password")
        superuser = request.POST.get("superuser")

        if superuser == "on":
            super = 1
        else:
            super = 0

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_handlelogin where UserName = '" + username + "' and UserPassword = '" + password + "'")
        user_cursor = dictfetchall(cursor)

        if len(user_cursor) == 0:

            duplicate_error = 0

            obj = HandleLogin(UserName = username, UserPassword = password, superuser = super)
            obj.save()

            return HttpResponseRedirect("/userlist")
        else:
            pval = request.POST
            print(pval)
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "add user"}
            return render(request, 'adduser.html', context)

    context = {'pagetitle': "add user"}

    return render(request, 'adduser.html', context)

def edituser(request, id):

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password")
        superuser = request.POST.get("superuser")

        if superuser == "on":
            super = 1
        else:
            super = 0

        print(superuser)

        obj = HandleLogin(LoginID = id, UserName = username, UserPassword = password, superuser = super)
        obj.save()

        return HttpResponseRedirect("/userlist")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_handlelogin where LoginID = " + str(id))
    r = dictfetchall(cursor)

    context = {'user': r,'pagetitle': "add user"}

    return render(request, 'edituser.html', context)

def deleteuser(request,id):

    if request.method == 'POST':
        log = HandleLogin.objects.get(pk=id)
        log.delete()
        return HttpResponseRedirect('/userlist')


def sample(request):

    session_user = request.session.get('userid','nouser')
    if (session_user == "nouser"):
        return HttpResponseRedirect("login")    

    return render(request,'page1.html')

def department(request):

    d1 = Department.objects.all()

    context = { 'dep' : d1 , 'pagetitle': "Department"}

    return render(request, 'department.html', context)


def adddepartment(request):

    duplicate_error = 0

    if request.method == "POST":
        
        name = request.POST.get('dname')

        name = name.capitalize()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_department where DepartmentName = '" + name + "'")
        department_cursor = dictfetchall(cursor)

        if len(department_cursor) == 0:

            duplicate_error = 0
            department = Department(DepartmentName = name)
            department.save()
            return redirect("/Department")
        else:
            pval = request.POST
            print(pval)
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "Add Department"}
            return render(request, 'adddepartment.html', context)

    return render(request, 'adddepartment.html', {'pagetitle': "Add Department"})

def editdepartment(request,DepartmentID):

    if request.method == "POST":
        name = request.POST.get('dname')

        department = Department(DepartmentID = DepartmentID ,DepartmentName = name)
        department.save()
        return HttpResponseRedirect("/Department")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_department where DepartmentID = " + str(DepartmentID))
        read = dictfetchall(cursor)

        
    return render(request, 'editdepartment.html', {'dep' : read , 'pagetitle': "Edit Department"})

def deletedepartment(request,id):

    if request.method == 'POST':
        dep = Department.objects.get(pk=id)
        dep.delete()
        return HttpResponseRedirect('/Department')


def specialization(request):

    s1 = Specialization.objects.all()

    context = { 'spe' : s1 , 'pagetitle': "Specialization"}

    return render(request, 'specialization.html', context)

def addspecialization(request):

    duplicate_error = 0

    if request.method == "POST":
        
        name = request.POST.get('name')
        name = name.capitalize()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_specialization where SpecializationName = '" + name + "'")
        specialization_cursor = dictfetchall(cursor)

        if len(specialization_cursor) == 0:

            duplicate_error = 0

            obj = Specialization(SpecializationName = name)
            obj.save()
            return redirect("/Specialization")
        else:
            pval = request.POST
            print(pval)
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "Add Specialization"}
            return render(request, 'addspecialization.html', context)

    return render(request, 'addspecialization.html', {'pagetitle': "Add Specialization"})

def editspecialization(request,id):

    if request.method == "POST":
        name = request.POST.get('name')

        model_obj = Specialization(SpecializationID = id ,SpecializationName = name)
        model_obj.save()
        return HttpResponseRedirect("/Specialization")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_specialization where SpecializationID = " + str(id))
        read = dictfetchall(cursor)

        
    return render(request, 'editspecialization.html', {'obj' : read , 'pagetitle': "Edit Specialization"})

def deletespecialization(request,id):

    if request.method == 'POST':
        model_obj = Specialization.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/Specialization')



# Gender

def gender(request):

    model_obj = Gender.objects.all()

    context = { 'obj' : model_obj , 'pagetitle': "Gender"}

    return render(request, 'gender.html', context)

def addgender(request):

    duplicate_error = 0

    if request.method == "POST":
        
        name = request.POST.get('name')

        name = name.capitalize()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_gender where GenderName = '" + name + "'")
        specialization_cursor = dictfetchall(cursor)

        if len(specialization_cursor) == 0:

            duplicate_error = 0

            obj = Gender(GenderName = name)
            obj.save()
            return redirect("/Gender")
        else:
            pval = request.POST
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "Add Gender"}
            return render(request, 'addgender.html', context)


    return render(request, 'addgender.html', {'pagetitle': "Add Gender"})

def editgender(request,id):

    if request.method == "POST":
        name = request.POST.get('name')

        model_obj = Gender(GenderID = id ,GenderName = name)
        model_obj.save()
        return HttpResponseRedirect("/Gender")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_gender where GenderID = " + str(id))
        read = dictfetchall(cursor)

        
    return render(request, 'editgender.html', {'obj' : read, 'pagetitle': "Edit Gender"})

def deletegender(request,id):

    if request.method == 'POST':
        model_obj = Gender.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/Gender')


# State

def state(request):

    model_obj = States.objects.all()

    context = { 'obj' : model_obj , 'pagetitle': "State"}

    return render(request, 'state.html', context)

def addstate(request):

    duplicate_error = 0

    if request.method == "POST":
        
        name = request.POST.get('name')

        name = name.capitalize()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_states where StateName = '" + name + "'")
        state_cursor = dictfetchall(cursor)


        if len(state_cursor) == 0:

            duplicate_error = 0

            obj = States(StateName = name)
            obj.save()
            return redirect("/States")
        else:
            pval = request.POST
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "Add State"}
            return render(request, 'addstate.html', context)

    return render(request, 'addstate.html', {'pagetitle': "Add State"})

def editstate(request,id):

    if request.method == "POST":
        name = request.POST.get('name')

        model_obj = States(StateID = id ,StateName = name)
        model_obj.save()
        return HttpResponseRedirect("/States")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_states where StateID = " + str(id))
        read = dictfetchall(cursor)
        
    return render(request, 'editstate.html', {'obj' : read, 'pagetitle': "Edit State"})

def deletestate(request,id):

    if request.method == 'POST':
        model_obj = States.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/States')


# Room Type

def roomtype(request):

    model_obj = RoomType.objects.all()

    context = { 'obj' : model_obj}

    return render(request, 'roomtype.html', context)

def addroomtype(request):
    if request.method == "POST":
        
        name = request.POST.get('name')

        obj = RoomType(RoomTypeName = name)
        obj.save()
        return redirect("/roomtype")

    return render(request, 'addroomtype.html')

def editroomtype(request,id):

    if request.method == "POST":
        name = request.POST.get('name')

        model_obj = RoomType(RoomTypeID = id ,RoomTypeName = name)
        model_obj.save()
        return HttpResponseRedirect("/roomtype")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_roomtype where RoomTypeID = " + str(id))
        read = dictfetchall(cursor)

        
    return render(request, 'editroomtype.html', {'obj' : read})

def deleteroomtype(request,id):

    if request.method == 'POST':
        model_obj = RoomType.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/roomtype')

#Patients

def patient(request):

    model_obj = Patients.objects.all()

    cursor = connection.cursor()
    cursor.execute("SELECT h1_patients.*, h1_gender.GenderName FROM h1_patients LEFT OUTER JOIN h1_gender on h1_patients.Gender_id = h1_gender.GenderID ORDER BY h1_patients.PatientID DESC")
    r = dictfetchall(cursor)

    print(r)

    context = { 'obj' : model_obj,
                'read': r , 'pagetitle': "Patient Master"}

    return render(request, 'patient.html', context)

def addnewpatient(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_gender")
    rgen = dictfetchall(cursor)

    duplicate_error = 0

    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        dob = request.POST.get('date')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        email = request.POST.get('email')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_patients where Mobile = '" + mobile + "' and DOB = '" + dob + "'")
        r = dictfetchall(cursor)

        print(r)

        if len(r) == 0:
            duplicate_error = 0
            if len(request.FILES) != 0:
                uploaded_file = request.FILES['Document']

                prev_file = uploaded_file.name
                split_file = prev_file.split(".")

                len_split_file = len(split_file)

                split_file_var = split_file[len_split_file - 1]

                file_name = firstname + "-" + mobile + "." + split_file_var

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "patient"))
                fs.save(file_name, uploaded_file)
            else:
                file_name = ""

            dob = str(dob)

            day = dob[8:10]
            month = dob[5:7]
            year = dob[0:4]

            dob = year + "-" + month + "-" + day

            obj = Patients(FirstName = firstname, Email = email, MiddleName = middlename, LastName = lastname, Gender = Gender.objects.get(GenderName = gender), DOB = dob, Mobile = mobile, PatientAddress = address, PatientImage = file_name)
            obj.save()

            consent = "I consent to participate in any research purpose. I also agree to let this data be used for any research purpose."

            #EMAIL
            subject = "Consent Approval"
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM h1_patients where Mobile = '" + mobile + "'")
            r = dictfetchall(cursor)

            patient_id = r[0]['PatientID']

            html_message = render_to_string('consentletter.html', {'id': patient_id})

            plain_message = strip_tags(html_message)

            from_email = "hospitalpro123@gmail.com"

            to_email = email

            send_mail(subject, plain_message,from_email,[to_email], html_message=html_message)

            return redirect("/Patients")
        else:
            pval = request.POST
            duplicate_error = 1
            context = {'gen' : rgen,"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error}
            return render(request, 'addnewpatient.html', context)

    return render(request, 'addnewpatient.html', {'gen' : rgen, 'pagetitle': "Add Patient"})

def approvepatient(request,PatientID):
    
    consent = 1

    date = datetime.date.today()

    date = str(date)

    day = date[8:10]
    month = date[5:7]
    year = date[0:4]

    date = year + "-" + month + "-" + day


    cursor = connection.cursor()
    cursor.execute("UPDATE h1_patients SET Consent = '"+ str(consent) +"', ApprovalDate = '"+ date +"' where PatientID = " + str(PatientID))

    return render(request, 'thankspage.html')


def editnewpatient(request,id):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_patients left outer join h1_gender on h1_patients.Gender_id = h1_gender.GenderID where PatientID = " + str(id))
    read = dictfetchall(cursor)

    date = ""

    for i in read:
        counter = 1

    print(i)

    for r in read:
        date = r["DOB"]

    date = str(date)

    day = date[8:10]
    month = date[5:7]
    year = date[0:4]

    date = year + "-" + month + "-" + day


    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM h1_gender")
    rgen = dictfetchall1(cursor1)

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        dob = request.POST.get('date')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        email = request.POST.get('email')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_patients where Mobile = '" + mobile + "' and DOB = '" + dob + "' and not PatientID = " + str(id))
        r = dictfetchall(cursor)

        if len(r) == 0:
            duplicate_error = 0

            if len(request.FILES) != 0:
                uploaded_file = request.FILES['Document']

                prev_file = uploaded_file.name
                split_file = prev_file.split(".")

                len_split_file = len(split_file)

                split_file_var = split_file[len_split_file - 1]

                file_name = firstname + "-" + mobile + "." + split_file_var

                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, "patient/"+file_name)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, "patient/"+file_name))
                    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "patient"))
                    fs.save(file_name, uploaded_file)
                else:
                    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "patient"))
                    fs.save(file_name, uploaded_file)

                dob = str(dob)

                day = dob[8:10]
                month = dob[5:7]
                year = dob[0:4]

                dob = year + "-" + month + "-" + day

                obj = Patients( PatientID = id, Email = email,FirstName = firstname, MiddleName = middlename, LastName = lastname, Gender = Gender.objects.get(GenderName = gender), DOB = dob, Mobile = mobile, PatientAddress = address, PatientImage = file_name)
                obj.save()
                
            elif len(request.FILES) == 0:
                dob = str(dob)

                obj = Patients.objects.get(pk = id)
                file_name = obj.PatientImage
                day = dob[8:10]
                month = dob[5:7]
                year = dob[0:4]

                dob = year + "-" + month + "-" + day

                obj = Patients( PatientID = id, Email = email,FirstName = firstname, MiddleName = middlename, LastName = lastname, Gender = Gender.objects.get(GenderName = gender), DOB = dob, Mobile = mobile, PatientAddress = address, PatientImage = file_name)
                obj.save()

            return HttpResponseRedirect("/Patients")
            # if len(request.FILES) !=0:
            #     if()
                
            #os.remove(os.path.join(settings.MEDIA_ROOT, "patient/"+file_name))
        else:
            pval = request.POST
            duplicate_error = 1

            context = {'gen' : rgen,"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error}
            return render(request, 'editnewpatient.html', context)

        
    return render(request, 'editnewpatient.html', {'i' : i, 'gen' : rgen, 'date': date, 'pagetitle': "Edit Patient"})

def deletenewpatient(request,id):

    if request.method == 'POST':

        cursor = connection.cursor()
        cursor.execute("SELECT h1_patients.*, h1_appointment.*, if(h1_appointment.AppointmentID = \'None\', 1, 0) as 'app_status' from h1_patients left outer join h1_appointment on h1_patients.PatientID = h1_appointment.Patient_id where h1_patients.PatientID = " + str(id))
        r = dictfetchall(cursor)

        num = r[0]['AppointmentID']
        print(num)


        num_2 = r[0]['app_status']
        #print(num_2)

        print(r)

        if(num == None):
            model_obj = Patients.objects.get(pk=id)
            model_obj.delete()
            return HttpResponseRedirect('/Patients')
        else:
            model_obj = Patients.objects.all()

            cursor = connection.cursor()
            cursor.execute("SELECT h1_patients.*, h1_gender.GenderName FROM h1_patients LEFT OUTER JOIN h1_gender on h1_patients.Gender_id = h1_gender.GenderID ORDER BY h1_patients.PatientID DESC")
            pat = dictfetchall(cursor)

            counter_delete_error = 1

            context = { 'obj' : model_obj,
                        'read': pat , 'pagetitle': "Patient Master", 
                        "delete_error": counter_delete_error}

            return render(request, 'patient.html', context)


def patientpreview(request, id):
    model_obj = Patients.objects.all()

    cursor = connection.cursor()
    cursor.execute("SELECT h1_patients.*, h1_gender.GenderName FROM h1_patients LEFT OUTER JOIN h1_gender on h1_patients.Gender_id = h1_gender.GenderID where PatientID = " + str(id))
    r = dictfetchall(cursor)

    print(r)

    cursor = connection.cursor()
    cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_patients.PatientID = " + str(id))
    a = dictfetchall(cursor)

    for i in a:
        date = i['AppointmentDate']

    date_t = datetime.datetime.now()

    date_t = str(date_t)

    date_t = date_t[0:10]

    context = { 'obj' : model_obj, 'read': r, 'appointment': a, 'pagetitle': "Patient Perview"}

    return render(request, 'patientpreview.html', context)

#Doctors

def doctor(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_doctors LEFT OUTER JOIN h1_gender on h1_doctors.Gender_id = h1_gender.GenderID LEFT OUTER JOIN h1_department on h1_doctors.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_specialization on h1_doctors.Specialization_id = h1_specialization.SpecializationID")
    r = dictfetchall(cursor)

    context = {'read': r, 'pagetitle': "Doctor Master"}

    return render(request, 'doctor.html', context)

def adddoctor(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_gender")
    r = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_department")
    dep = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_specialization")
    spe = dictfetchall(cursor)

    duplicate_error = 0

    if request.method == "POST":
        
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        joindate = request.POST.get('date')
        department = request.POST.get('department')
        specialization = request.POST.get('specialization')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_doctors where Mobile = '" + mobile + "'")
        error = dictfetchall(cursor)

        if len(error) == 0:

            duplicate_error = 0

            joindate = str(joindate)

            day = joindate[8:10]
            month = joindate[5:7]
            year = joindate[0:4]

            date = year + "-" + month + "-" + day

            obj = Doctors(FirstName = firstname, MiddleName = middlename, LastName = lastname, Specialization = Specialization.objects.get(SpecializationName = specialization), Gender = Gender.objects.get(GenderName = gender), JoiningDate = date, Department = Department.objects.get(DepartmentName = department), Mobile = mobile, DoctorAddress = address)
            obj.save()
            return redirect("/Doctor")
        else:
            dval = request.POST
            print(dval)
            duplicate_error = 1
            context = {'gen' : r, 'dep': dep,'spe': spe,  'error_counter' : duplicate_error, 'pagetitle': "Add Doctor", "dval":dval, "error": "Duplicate record found!!"}
            return render(request, 'adddoctor.html', context)


    return render(request, 'adddoctor.html', {'gen' : r, 'dep': dep,'spe': spe,  'error_counter' : duplicate_error, 'pagetitle': "Add Doctor"})

def editdoctor(request,id):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_doctors LEFT OUTER JOIN h1_gender on h1_doctors.Gender_id = h1_gender.GenderID LEFT OUTER JOIN h1_department on h1_doctors.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_specialization on h1_doctors.Specialization_id = h1_specialization.SpecializationID where DoctorID = " + str(id))
    read = dictfetchall(cursor)
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_gender")
    rgen = dictfetchall1(cursor)

    date = ""

    for i in read:
        counter = 1

    for r in read:
        date = r["JoiningDate"]


    date = str(date)

    day = date[8:10]
    month = date[5:7]
    year = date[0:4]

    date = year + "-" + month + "-" + day

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_specialization")
    spe = dictfetchall1(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_department")
    dep = dictfetchall1(cursor)

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        joindate = request.POST.get('date')
        department = request.POST.get('department')
        specialization = request.POST.get('specialization')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        joindate = str(joindate)

        day = joindate[8:10]
        month = joindate[5:7]
        year = joindate[0:4]

        date = year + "-" + month + "-" + day

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_doctors where Mobile = '" + mobile + "' and not DoctorID = " + str(id))
        r = dictfetchall(cursor)

        if len(r) == 0:
            duplicate_error = 0

            obj = Doctors(DoctorID = id ,FirstName = firstname, MiddleName = middlename, LastName = lastname, Specialization = Specialization.objects.get(SpecializationName = specialization), Gender = Gender.objects.get(GenderName = gender), JoiningDate = date, Department = Department.objects.get(DepartmentName = department), Mobile = mobile, DoctorAddress = address)
            obj.save()
            return redirect("/Doctor")
        else:
            dval = request.POST
            print(dval)
            duplicate_error = 1
            context = {'gen' : rgen, 'dep': dep,'spe': spe,'id': id ,  'error_counter' : duplicate_error, 'pagetitle': "Edit Doctor", "dval":dval, "error": "Duplicate record found!!"}
            return render(request, 'editdoctor.html', context)

        
    return render(request, 'editdoctor.html', {'i' : i,'id': id, 'gen' : rgen, 'spe' : spe, 'dep' : dep, 'date' : date, 'pagetitle': "Edit Doctor"})

def deletedoctor(request,id):

    if request.method == 'POST':
        model_obj = Doctors.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/Doctor')


# Time

def time(request):

    model_obj = Time.objects.all()

    context = { 'obj' : model_obj, 'pagetitle': "Time"}

    return render(request, 'time.html', context)

def addtime(request):
    duplicate_error = 0
    if request.method == "POST":
        
        time = request.POST.get('time')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_time where Time = '" + time + "'")
        time_cursor = dictfetchall(cursor)

        print(time_cursor)

        if len(time_cursor) == 0:

            duplicate_error = 0

            obj = Time(Time = time)
            obj.save()
            return redirect("/Time")
        else:
            pval = request.POST
            print(pval)
            duplicate_error = 1
            context = {"pval":pval,"error": "Duplicate record found!!", 'error_counter' : duplicate_error,'pagetitle': "Add Time"}
            return render(request, 'addtime.html', context)

    return render(request, 'addtime.html', {'pagetitle': "Add Time"})

def edittime(request,id):

    if request.method == "POST":
        time = request.POST.get('time')

        model_obj = Time(TimeID = id ,Time = time)
        model_obj.save()
        return HttpResponseRedirect("/Time")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_time where TimeID = " + str(id))
        read = dictfetchall(cursor)

        for r in read:
            time = r['Time']

        time = str(time)

        hh = time[0:2]
        mm = time[3:5]

        time = hh + ":" + mm
        
    return render(request, 'edittime.html', {'obj' : read, 'time': time, 'pagetitle': "Edit Time"})

def deletetime(request,id):

    if request.method == 'POST':
        model_obj = Time.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/Time')



#Appointment

def appointment(request):
    cursor = connection.cursor()
    cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID")
    r = dictfetchall(cursor)

    for i in r:
        date = i['AppointmentDate']

    date_t = datetime.datetime.now()

    date_t = str(date_t)

    date_t = date_t[0:10]

    if request.method == 'POST':
        method = request.POST.get('filter')

        if method == "All":
            cursor = connection.cursor()
            cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID")
            r = dictfetchall(cursor)

            context = {'read': r, 'pagetitle': "All Appointments", 'clsinprocess':'btn-primary', 'clsfuture':'btn-primary','clscompleted':'btn-primary','clscancelled':'btn-primary','clsall':'btn-success' }

            return render(request, 'appointment.html', context)
        elif method == "Future":
            cursor = connection.cursor()
            cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_appointment.AppointmentDate > CURRENT_DATE() and h1_appointment.Status = \'Active\'")
            r = dictfetchall(cursor)

            context = {'read': r , 'pagetitle': "Future Appointments", 'clsinprocess':'btn-primary', 'clsfuture':'btn-success','clscompleted':'btn-primary','clscancelled':'btn-primary','clsall':'btn-primary' }

            return render(request, 'appointment.html', context)
        elif method == "In Process":
            cursor = connection.cursor()
            cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_appointment.AppointmentDate <= CURRENT_DATE() and h1_appointment.Status = \'Active\'")
            r = dictfetchall(cursor)

            context = {'read': r , 'pagetitle': "InProcess Appointments", 'clsinprocess':'btn-success', 'clsfuture':'btn-primary','clscompleted':'btn-primary','clscancelled':'btn-primary','clsall':'btn-primary' }

            return render(request, 'appointment.html', context)
        elif method == "Completed":
            cursor = connection.cursor()
            cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_appointment.Status = \'Completed\'")
            r = dictfetchall(cursor)

            context = {'read': r , 'pagetitle': "Completed Appointments", 'clsinprocess':'btn-primary', 'clsfuture':'btn-primary','clscompleted':'btn-success','clscancelled':'btn-primary','clsall':'btn-primary' }

            return render(request , 'appointment.html', context)
        elif method == "Cancelled":
            cursor = connection.cursor()
            cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_appointment.Status = \'Cancelled\'")
            r = dictfetchall(cursor)

            context = {'read': r , 'pagetitle': "Cancelled Appointments", 'clsinprocess':'btn-primary', 'clsfuture':'btn-primary','clscompleted':'btn-primary','clscancelled':'btn-success','clsall':'btn-primary' }

            return render(request, 'appointment.html', context)

    context = {'read': r , 'pagetitle': "All Appointments", 'clsinprocess':'btn-primary', 'clsfuture':'btn-primary','clscompleted':'btn-primary','clscancelled':'btn-primary','clsall':'btn-primary' }

    return render(request, 'appointment.html', context)

def addappointment(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_patients")
    p = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_time")
    time_cursor = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_department")
    dep = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_doctors")
    doc = dictfetchall(cursor)
    
    #max="2019-12-25"
    duplicate_error = 0
    
    today = datetime.date.today()
    day_add = datetime.timedelta(days = 20)

    max_date = today + day_add
    date_now = datetime.date.today()

    date_now = str(date_now)
    max_date = str(max_date)

    if request.method == "POST":
        
        patient = request.POST.get('patient')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        time = request.POST.get('time')
        date = request.POST.get('date')
        problem = request.POST.get('problem')

        cursor = connection

        cursor = connection.cursor()
        a = "SELECT * FROM h1_appointment where AppointmentDate = '" + date + "' and Time_id = '"+ time + "' and Doctor_id = '" + doctor + "'"
        cursor.execute(a)
        error = dictfetchall(cursor)

        if len(error) == 0:

            duplicate_error = 0
            date = str(date)

            day = date[8:10]
            month = date[5:7]
            year = date[0:4]

            date = year + "-" + month + "-" + day

            obj = Appointment(Patient = Patients.objects.get(PatientID = patient), Doctor = Doctors.objects.get(DoctorID = doctor), Department = Department.objects.get(DepartmentID = department), Time = Time.objects.get(TimeID = time), Problem = problem, AppointmentDate = date, Status = "Active")
            obj.save()
            return redirect("/Appointment")
        else:
            aval = request.POST
            print("New")
            print(aval)
            patient = int(aval['patient'])
            doctor = int(aval['doctor'])
            department = int(aval['department'])
            time_new = int(aval['time'])
            duplicate_error = 1
            context = {'pat' : p,'doc': doc, 'dep': dep, 'time': time_cursor,'department': department, 'time_new': time_new, 'patient':patient, 'doctor': doctor, 'error_counter' : duplicate_error, 'pagetitle': "Add Appointment", "aval":aval, "error": "Duplicate record found!!", 'max_date': max_date, 'date_now': date_now}
            return render(request, 'addappointment.html', context)


    return render(request, 'addappointment.html', {'pat' : p, 'pagetitle': "Add Appointments", 'dep': dep,'doc': doc, 'time': time_cursor, 'max_date': max_date, 'date_now': date_now})

def editappointment(request,id):

    if request.method == "POST":
        patient = request.POST.get('patient')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        time = request.POST.get('time')
        date = request.POST.get('date')
        problem = request.POST.get('problem')


        date = str(date)

        day = date[8:10]
        month = date[5:7]
        year = date[0:4]

        date = year + "-" + month + "-" + day

        obj = Appointment(AppointmentID = id, AppointmentDate = date, Patient = Patients.objects.get(PatientID = patient), Doctor = Doctors.objects.get(DoctorID = doctor), Department = Department.objects.get(DepartmentID = department), Time = Time.objects.get(TimeID = time), Problem = problem)
        obj.save()
        return redirect("/Appointment")
    else:
        cursor = connection.cursor()
        a = "SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where AppointmentID = "+ str(id)
        cursor.execute(a)
        r = dictfetchall(cursor)
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_patients")
        pat = dictfetchall1(cursor)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_department")
        dep = dictfetchall1(cursor)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_doctors")
        doc = dictfetchall1(cursor)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM h1_time")
        time = dictfetchall1(cursor)

        date = ""

        for q in r:
            date = q["AppointmentDate"]

        date = str(date)

        day = date[8:10]
        month = date[5:7]
        year = date[0:4]

        date = year + "-" + month + "-" + day

    return render(request, 'editappointment.html', {'read' : r, 'pat' : pat, 'pagetitle': "Edit Appointments", 'doc' : doc, 'dep' : dep, 'time' : time, 'date' : date})

def deleteappointment(request,id):

    if request.method == 'POST':
        model_obj = Appointment.objects.get(pk=id)
        model_obj.delete()
        return HttpResponseRedirect('/Appointment')

def cancelappointment(request,id):

    if request.method == 'POST':

        cursor = connection.cursor()
        a = "UPDATE h1_appointment SET Status = \'Cancelled\' where AppointmentID = "+ str(id)
        cursor.execute(a)

        return HttpResponseRedirect('/Appointment')

def processappointment(request,id):

    if request.method == "POST":
        prescription = request.POST.get('prescription')
        report = request.POST.get('report')
        problem = request.POST.get('problem')

        cursor = connection.cursor()
        cursor.execute("UPDATE h1_appointment SET Prescription = '" + prescription +"', Report = '" + report +"', Problem = '" + problem + "', Status = 'Completed' where AppointmentID = "+ str(id))
        return redirect("/Appointment")
    cursor = connection.cursor()
    a = "SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where AppointmentID = "+ str(id)
    cursor.execute(a)
    r = dictfetchall(cursor)
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_patients")
    pat = dictfetchall1(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_department")
    dep = dictfetchall1(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_doctors")
    doc = dictfetchall1(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_time")
    time = dictfetchall1(cursor)

    date = ""

    read = r

    for q in read:
        date = q["AppointmentDate"]
    
    date = str(date)

    day = date[8:10]
    month = date[5:7]
    year = date[0:4]

    date = year + "-" + month + "-" + day

    return render(request, 'processappointment.html', {'read' : r, 'pagetitle': "Process Appointments", 'pat' : pat, 'doc' : doc, 'dep' : dep, 'time' : time, 'date' : date})


def printprescription(request,id):
    
    cursor = connection.cursor()
    cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo', h1_patients.Gender_id as 'pg' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where AppointmentID = "+ str(id))
    r = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM h1_gender where GenderID = " + str(r[0]['pg']))
    g = dictfetchall(cursor)

    Pfirstname = r[0]['pf']
    Pmiddlename = r[0]['pm']
    Plastname = r[0]['pl']
    Pmobile = r[0]['pmo']
    Dfirstname = r[0]['df']
    Dmiddlename = r[0]['dm']
    Dlastname = r[0]['dl']
    Dmobile = r[0]['m']
    gender = g[0]['GenderName']
    Department = r[0]['DepartmentName']
    AppointmentDate = r[0]['AppointmentDate']
    Time = r[0]['Time']
    problem = r[0]['Problem']
    prescription = r[0]['Prescription']
    reports = r[0]['Report']

    with open(os.path.join(os.path.join(settings.BASE_DIR, "static"), "report_formats\\reports.html"), 'r') as temp:
        content = temp.read()
        content = content.replace("{{FirstName}}",Pfirstname)
        content = content.replace("{{MiddleName}}",Pmiddlename)
        content = content.replace("{{LastName}}",Plastname)
        content = content.replace("{{Gender}}",gender)
        content = content.replace("{{DMobile}}",Dmobile)
        content = content.replace("{{DepartmentName}}",Department)
        content = content.replace("{{AppointmentDate}}",str(AppointmentDate))
        content = content.replace("{{Time}}",str(Time))
        content = content.replace("{{DFirstName}}",Dfirstname)
        content = content.replace("{{DMiddleName}}",Dmiddlename)
        content = content.replace("{{DLastName}}",Dlastname)
        content = content.replace("{{Problem}}",problem)

        strprescription = prescription
        arrp = strprescription.split('\n')
        
        strpdata = "<ul>"
        for r in arrp:
            strpdata += "<li>" + r + "</li>"

        strpdata += "</ul>"

        strreport = reports
        arrr = strreport.split('\n')

        strrdata = "<ul>"

        for q in arrr:
            strrdata += "<li>" + q + "</li>"

        strrdata += "</ul>"         

        content = content.replace("{{Prescription}}",strpdata)
        content = content.replace("{{Report}}",strrdata)

    
    file_name = Pfirstname + "_" + str(id) + ".pdf"

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(content, os.path.join(settings.MEDIA_ROOT, "prescription\\"+ file_name), configuration=config)

    with open(os.path.join(settings.MEDIA_ROOT, "prescription\\" + file_name), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=' + file_name
        return response



def appointmentpreview(request,id):
    cursor = connection.cursor()
    cursor.execute("SELECT *, h1_doctors.FirstName as 'df', h1_doctors.MiddleName as 'dm', h1_doctors.LastName as 'dl', h1_doctors.Mobile as 'm', h1_patients.FirstName as 'pf', h1_patients.MiddleName as 'pm', h1_patients.LastName as 'pl', h1_patients.Mobile as 'pmo', h1_patients.Gender_id as 'pg',if(h1_appointment.AppointmentDate<=current_date(),\"IN_PROCESS\",\"FUTURE_DATE\") as 'DateStatus' FROM h1_appointment LEFT OUTER JOIN h1_patients on h1_appointment.Patient_id = h1_patients.PatientID LEFT OUTER JOIN h1_doctors on h1_appointment.Doctor_id = h1_doctors.DoctorID LEFT OUTER JOIN h1_department on h1_appointment.Department_id = h1_department.DepartmentID LEFT OUTER JOIN h1_time on h1_appointment.Time_id = h1_time.TimeID where h1_appointment.AppointmentID = " + str(id))
    r = dictfetchall(cursor)


    for j in r:
        genderid = j['pg']

    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM h1_gender where GenderID = " + str(genderid))
    patientgender = dictfetchall(cursor)

    for k in patientgender:
        gender = k['GenderName']

    for i in r:
        date = i['AppointmentDate']

    date_t = datetime.datetime.now()

    date_t = str(date_t)

    date_t = date_t[0:10]

    context = {'read': r, 'gender': gender, 'pagetitle': "Preview Appointments"}

    return render(request, 'appointmentpreview.html', context)
from django.urls import path
from H1 import views

urlpatterns = [
    path('', views.index, name = 'HospitalManagement'),
    path('PatientApproval/<int:PatientID>', views.approvepatient, name = 'ApprovePatient'),
    path('addpatient', views.addpatient, name = 'AddPatient'),
    path('editpatient/<int:PatientID>', views.editpatient, name = 'EditPatient'),
    path('deletepatient/<int:id>', views.deletepatient, name = 'DeletePatient'),
    path('medicines', views.medicines, name="Medicines"),
    path('login', views.login, name='Login'),
    path('logout', views.logout, name='logout'),
    path('userlist', views.userlist, name='userlist'),
    path('adduser', views.adduser, name='adduser'),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('sample', views.sample, name='Sample'),
    path('Department', views.department, name = 'department'),
    path('AddDepartment', views.adddepartment, name = 'adddepartment'),
    path('editdepartment/<int:DepartmentID>', views.editdepartment, name = 'editdepartment'),
    path('deletedepartment/<int:id>', views.deletedepartment, name = 'deletedepartment'),
    path('Specialization', views.specialization, name = 'specialization'),
    path('addspecialization', views.addspecialization, name = 'addspecialization'),
    path('editspecialization/<int:id>', views.editspecialization, name = 'editspecialization'),
    path('deletespecialization/<int:id>', views.deletespecialization, name = 'deletespecialization'),
    path('Gender', views.gender, name = 'gender'),
    path('addgender', views.addgender, name = 'addgender'),
    path('editgender/<int:id>', views.editgender, name = 'editgender'),
    path('deletegender/<int:id>', views.deletegender, name = 'deletegender'),
    #Hospital details
    path('Hospital/<int:id>', views.hospital, name = 'hospital'),
    #state
    path('States', views.state, name = 'state'),
    path('addstate', views.addstate, name = 'addstate'),
    path('editstate/<int:id>', views.editstate, name = 'editstate'),
    path('deletestate/<int:id>', views.deletestate, name = 'deletestate'),
    #roomtype
    path('roomtype', views.roomtype, name = 'roomtype'),
    path('addroomtype', views.addroomtype, name = 'addroomtype'),
    path('editroomtype/<int:id>', views.editroomtype, name = 'editroomtype'),
    path('deleteroomtype/<int:id>', views.deleteroomtype, name = 'deleteroomtype'),
    #patient
    path('Patients', views.patient, name = 'patient'),
    path('AddPatient', views.addnewpatient, name = 'addnewpatient'),
    path('editnewpatient/<int:id>', views.editnewpatient, name = 'editnewpatient'),
    path('deletenewpatient/<int:id>', views.deletenewpatient, name = 'deletenewpatient'),
    path('patientpreview/<int:id>', views.patientpreview, name = 'patientpreview'),
    #doctor
    path('Doctor', views.doctor, name = 'doctor'),
    path('AddDoctor', views.adddoctor, name = 'adddoctor'),
    path('editdoctor/<int:id>', views.editdoctor, name = 'editdoctor'),
    path('deletedoctor/<int:id>', views.deletedoctor, name = 'deletedoctor'),
    #timeslot
    path('Time', views.time, name = 'time'),
    path('addtime', views.addtime, name = 'addtime'),
    path('edittime/<int:id>', views.edittime, name = 'edittime'),
    path('deletetime/<int:id>', views.deletetime, name = 'deletetime'),
    #appointment
    path('Appointment', views.appointment, name = 'appointment'),
    path('AddAppointment', views.addappointment, name = 'addappointment'),
    path('editappointment/<int:id>', views.editappointment, name = 'editappointment'),
    path('deleteappointment/<int:id>', views.deleteappointment, name = 'deleteappointment'),
    path('cancelappointment/<int:id>', views.cancelappointment, name = 'cancelappointment'),
    path('processappointment/<int:id>', views.processappointment, name = 'processappointment'),
    path('appointmentpreview/<int:id>', views.appointmentpreview, name = 'appointmentpreview'),
    path('printprescription/<int:id>', views.printprescription, name = 'printprescription'),
]


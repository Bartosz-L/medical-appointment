from django.urls import path
from . import views

app_name = 'appointments_app'
urlpatterns = [
    # index view
    path('', views.IndexView.as_view(), name='index'),
    # registration
    path('registration/', views.registration, name='registration'),
    path('registration/create', views.createPatientLogIn, name='createPatientLogIn'),
    # password
    path('password/', views.password, name='password'),
    path('password/changepass/', views.changePass, name='changepass'),
    path('verify/', views.verify, name='verify'),
    # logs, stats, logout
    path('log/', views.log, name='log'),
    path('statistics/', views.statistics, name='statistics'),
    path('logout/', views.logout, name='logout'),
    # home view
    path('home/', views.home, name='home'),
    path('home/register-doctor-nurse', views.registerDoctorNurse, name='registerDoctorNurse'),
    path('home/register-doctor-nurse/create-doctor-nurse', views.createDoctorNurseLogIn, name='createDoctorNurseLogIn'),
    # info view
    path('information/', views.information, name='information'),
    path('information/update-profile', views.updateProfile, name='updateProfile'),
    path('information/update-profile/update-profile-info', views.updateProfileInfo, name='updateProfileInfo'),
    path('information/update-med/<int:pat_id>/', views.updateMed, name='updateMed'),
    path('information/update-med/update-med-info/<int:pat_id>/', views.updateMedInfo, name='updateMedInfo'),
    path('information/export', views.export, name='export'),
    path('information/discharge/<int:pat_id>', views.discharge, name='discharge'),
    path('information/admission/<int:pat_id>/<int:emp_id>', views.admission, name='admission'),
    path('information/transfer/<int:pat_id>/<int:emp_id>', views.transfer, name='transfer'),
    path('information/tests/<int:pat_id>/', views.tests, name='tests'),
    path('information/tests/create-test/<int:pat_id>/', views.createTest, name='createTest'),
    path('information/tests/create-test/create-test-info/<int:pat_id>/', views.createTestInfo, name='createTestInfo'),
    path('information/tests/release-test/<int:test_id>/', views.releaseTest, name='releaseTest'),
    path('information/test-details/<int:test_id>/', views.testDetails, name='testDetails'),
    # appointments view
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/create-appointment', views.createAppointment, name='createAppointment'),
    path('appointments/create-appointment/create-appointment-info', views.createAppointmentInfo,
         name='createAppointmentInfo'),
    path('appointments/update-appointment/<int:appt_id>/', views.updateAppointment, name='updateAppointment'),
    path('appointments/update-appointment/update-appointment-info/<int:appt_id>/', views.updateAppointmentInfo,
         name='updateAppointmentInfo'),
    path('appointments/cancel-appointment/<int:appt_id>/', views.cancelAppointment, name='cancelAppointment'),
    # prescriptions view
    path('prescriptions/$', views.prescriptions, name='prescriptions'),
    path('prescriptions/create-prescriptions', views.createPrescriptions, name='createPrescriptions'),
    path('prescriptions/create-prescriptions/create-prescriptions-info', views.createPrescriptionsInfo,
         name='createPrescriptionsInfo'),
    path('prescriptions/update-prescriptions/<int:pres_id>/', views.updatePrescriptions, name='updatePrescriptions'),
    path('prescriptions/update-prescriptions/update-prescriptions-info/<int:pres_id>/', views.updatePrescriptionsInfo,
         name='updatePrescriptionsInfo'),
    path('prescriptions/remove-prescriptions/<int:pres_id>/', views.removePrescriptions, name='removePrescriptions'),
    # calendar view
    path('calendar/', views.calendar, name='calendar'),
]

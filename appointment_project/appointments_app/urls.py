from django.urls import path
from . import views

app_name = 'appointments_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.registration, name='registration'),
    path('registration/create', views.createPatientLogIn, name='createPatientLogIn'),
    path('password/', views.password, name='password'),
    path('password/changepass/', views.changePass, name='changepass'),
    path('verify/', views.verify, name="verify"),
    path('home/', views.home, name="home"),
    path('home/register-doctor-nurse', views.registerDoctorNurse, name='registerDoctorNurse'),
    path('home/register-doctor-nurse/create-doctor-nurse', views.createDoctorNurseLogIn, name='createDoctorNurseLogIn'),
]

# imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.list import ListView
from .models import Test
from .models import Patient
from .models import EmergencyContact
from .models import Doctor
from .models import Nurse
from .models import Prescription
from .models import Hospital
from .models import Appointment
from .models import LogInInfo
from .models import Administrator
from .models import Message
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from datetime import date
import os
import csv

# This variable is for storing the username entered when a user logs-in
uname = ''


# modił przeprowadza logowanie aktywności poprzez zapis logów do pliku textowego,
# który póżniej jest renderowany w HTMLu dla administratora do wglądu
def logActivity(activity):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\appointments_app\\log\\" + filename, 'a')
    target.write(activity)
    target.write("\n")
    target.close()


# Widok odpowiada za generyczny templete view dla strony index,
# do której użytkownik będzie się logował, bądź rejestrował, jeżeli nie posiada konta
class IndexView(ListView):
    template_name = 'appointments_app/index.html'
    context_object_name = 'user_login_information'

    def get_queryset(self):
        return LogInInfo.objects.order_by('-username')


# Widok odpowiada za renderowanie HTMLa dla strony do rejestracji
def registration(request):
    return render(request, 'appointments_app/registration.html')


def createPatientLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    address = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceId = (request.POST['insuranceId'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    username = (request.POST['username'])
    password = (request.POST['password'])

    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        global uname
        uname = username
        try:
            contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname,
                                                   address=contactaddress, number=contactnumber)
        except ObjectDoesNotExist:
            contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber)
        Patient.objects.create(username=uname)
        patient = Patient.objects.get(username=uname)
        patient.firstName = firstName
        patient.lastName = lastName
        patient.address = address
        patient.number = number
        patient.email = email
        patient.provider = provider
        patient.insuranceId = insuranceId
        patient.contact = contact
        patient.height = height
        patient.weight = weight
        patient.allergies = allergies
        patient.gender = gender
        patient.save()

        activity = f'User {username} registered a new account - logged on: ' \
            f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
        logActivity(activity)
        return HttpResponseRedirect(reverse('appointments_app:home', args=()))
    else:
        return render(request, 'appointments_app/registration.html', {
            'username': username,
            'error_message': "Username already exists.",
        })


# widok renderuje HTML dla zmiany hasła
def password(request):
    return render(request, 'appointments_app/password.html')


# widok zajmuje się zmianą hasła użytkownika
def changePass(request):
    try:
        username = (request.POST['username'])
        newpass = (request.POST['password'])
        currinfo = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'appointments_app/password.html', {
            'username': username,
            'error_message': 'There was a problem with your username'
        })
    else:
        currinfo.password = newpass
        currinfo.save()
        activity = f'User {username} changed their password - logged on ' \
            f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
        logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:index', args=()))


# widok odpowiada za próbe logowania się użytkownika. Jeżeli nazwa użytkownika i hasło są poprawne
# wtedy użytkownik jest przenoszony do profilu. Jeżeli nie,
# generowany jest alert z błędem, a uzytkownik jest przekierowany do strony domowej
def verify(request):
    username = (request.POST['username'])
    passwordInput = (request.POST['password'])

    try:
        current = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'appointments_app/index.html', {
            'username': username,
            'error_message': 'There was a problem with your username',
        })
    else:
        passwordActual = current.password
        if passwordInput == passwordActual:
            global uname
            uname = username
            activity = f'User {username} logged in - logged on ' \
                f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
            logActivity(activity)
            return HttpResponseRedirect(reverse('appointments_app:home', args=()))
        else:
            return render(request, 'appointments_app/index.html', {
                'username': username,
                'error_message': 'There was a problem with your password',
            })


# widok renderuje html dla strony home wyświetlanej po zalogowaniu
def home(request):
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'appointments_app/index.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Administrator"
                    context = {'user': a,
                               'type': utype}
                    return render(request, 'appointments_app/home.html', context)
            else:
                utype = "Nurse"
                context = {'user': n,
                           'type': utype}
                return render(request, 'appointments_app/home.html', context)
        else:
            utype = "Doctor"
            context = {'user': d,
                       'type': utype}
            return render(request, 'appointments_app/home.html', context)
    else:
        utype = "Patient"
        context = {'user': p,
                   'type': utype}
        return render(request, 'appointments_app/home.html', context)


# widok odpowiada za renderowanie html'a dla rejestracji doktora i pielegniarki
def registerDoctorNurse(request):
    workplaces = Hospital.objects.order_by('-name')
    admin = Administrator.objects.get(username=uname)
    context = {'workplaces': workplaces, 'admin': admin}
    return render(request, 'appointments_app/registerDoctorNurse.html', context)


# widok odpowiada za rejestrację Doktora i Pielęgniarki. Moduł LogInInfo jest użyty do zachowania danych w bazie danych
def createDoctorNurseLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    type = (request.POST['type'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    admin = Administrator.objects.get(username=uname)
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        if type == 'Doctor':
            Doctor.objects.create(username=username, firstName=firstName, lastName=lastName)
            d = Doctor.objects.get(username=username)
            d.workplace = admin.workplace
            d.save()
            activity = f'Administrator {uname} registered a new doctor account - logged on: ' \
                f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
            logActivity(activity)
            return HttpResponseRedirect(reverse('appointments_app:home', args=()))
        elif type == 'Nurse':
            Nurse.objects.create(username=username, firstName=firstName, lastName=lastName)
            n = Nurse.objects.get(username=username)
            n.workplace = admin.workplace
            n.save()
            activity = f'Administrator {uname} registered a new Nurse account - logged on: ' \
                f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
            logActivity(activity)
            return HttpResponseRedirect(reverse('appointments_app:home', args=()))
        else:
            Administrator.objects.create(username=username, firstName=firstName, lastName=lastName)
            a = Administrator.objects.get(username=username)
            a.workplace = admin.workplace
            a.save()
            activity = f'Administrator {uname} registered a new Administrator account - logged on: ' \
                f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
            logActivity(activity)
            return HttpResponseRedirect(reverse('appointments_app:home', args=()))
    else:
        return render(request, 'appointments_app/registerDoctorNurse.html', {
            'username': username,
            'workplace': Hospital.objects.order_by("-name"),
            'error_message': "Username already exists.",
        })

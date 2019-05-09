from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from ..models import Patient
from ..models import EmergencyContact

from ..models import LogInInfo
from django.core.exceptions import ObjectDoesNotExist
import datetime
from .logActivity import logActivity

# zmienna przechowuje nazwe uzytkownika kiedy uzytkownik się loguje
uname = ''


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


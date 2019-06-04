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


# Widok przeprowadza logowanie aktywności poprzez zapis logów do pliku textowego,
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


# widok renderujący html z informacjami o użytkowniku
def information(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = 'Nurse'
                patients = Patient.objects.order_by("-lastName")
                patw = Patient.objects.filter(hospital=n.workplace)
                context = {'patients': patients,
                           'patw': patw,
                           'employee': n,
                           'type': utype}
                return render(request, 'appointments_app/information.html', context)
        else:
            utype = "Doctor"
            patients = Patient.objects.order_by("-lastName")
            patw = Patient.objects.filter(hospital=d.workplace)
            context = {'patients': patients,
                       'patw': patw,
                       'employee': d,
                       'type': utype}
            return render(request, 'appointments_app/information.html', context)
    else:
        utype = "Patient"
        tests = Test.objects.filter(patient=p)
        context = {'patient': p,
                   'type': utype,
                   'tests': tests}
        return render(request, 'appointments_app/information.html', context)


# Widok odpowiada za renderowanie htmla do edycji Profilu.
def updateProfile(request):
    global uname
    patient = Patient.objects.get(username=uname)
    context = {'patient': patient}
    return render(request, 'appointments_app/updateProfile.html', context)


# Widok zamuje się modyfikowaniem bazy dla profilu pacjenta.
# Po zapisaniu danych, użytkownik jest przenoszony do informacji o pacjencie.
def updateProfileInfo(request):
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
    try:
        contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                               number=contactnumber)
    except ObjectDoesNotExist:
        contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                                  number=contactnumber)
    patient = Patient.objects.get(username=uname)
    patient.firstName = firstName
    patient.lastName = lastName
    patient.address = address
    patient.number = number
    patient.email = email
    patient.provider = provider
    patient.insuranceid = insuranceid
    patient.contact = contact
    patient.save()

    activity = f'User {patient.username} updated their profile info - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:information', args=()))


# Widok renderuje HTML dla zmiany informacji medycznych o pacjencie.
def updateMed(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'appointments_app/updateMedInfo.html', context)


# Widok zamuje się modyfikowaniem bazy dla informacji medycznych o pacjencie.
# Po zapisaniu danych, użytkownik jest przenoszony do informacji o pacjencie.
def updateMedInfo(request, pat_id):
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    patient = Patient.objects.get(id=pat_id)
    patient.height = height
    patient.weight = weight
    patient.allergies = allergies
    patient.gender = gender
    patient.save()

    activity = f'User {uname} updated Patient {patient.username}\'s medical information - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:information', args=()))


# Widok zajmuje się eksportowaniem informacji o pacjencie do pliku CSV na lokalną maszynę.
def export(request):
    global uname
    patient = Patient.objects.get(username=uname)
    testResults = Test.objects.filter(patient=patient, released=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PatientInfo.csv"'
    filewriter = csv.writer(response)
    filewriter.writerow(['', 'Name', 'Email', 'Address', 'Phone Number', 'Insurance ID', 'Insurance Provider'])
    filewriter.writerow(
        ['Patient Profile Info:', patient.lastName + "," + patient.firstName, patient.email, patient.address,
         patient.number, patient.insuranceId, patient.provider])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Name', 'Address', 'Phone Number'])
    filewriter.writerow(['Patient Emergency Contact:', patient.contact.lastName + ", " + patient.contact.firstName,
                         patient.contact.address, patient.contact.number])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Height', 'Weight', 'Allergies', 'Gender'])
    filewriter.writerow(
        ['Patient Medical Information:', patient.height, patient.weight, patient.allergies, patient.gender])
    filewriter.writerow([''])
    filewriter.writerow(['Patient Test Information', 'Name', 'Doctor Notes', 'Doctor Name'])
    count = 1
    for test in testResults:
        filewriter.writerow(['Test ' + str(count), test.name, test.description, test.doctor])
        count += 1
    activity = f'User {patient.username} exported their information - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return response


# Widok odpowiada za usuwanie pacjenta ze szpitala.
def discharge(request, pat_id):
    patient = Patient.objects.get(id=pat_id)
    patient.hospital = None
    patient.save()
    return HttpResponseRedirect(reverse('appointments_app:information', args=()))


# Widok odpowiada za przypisywanie pacjenta do szpitala.
def admission(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('appointments_app:information', args=()))


# Widok zajmuje się transferem pacjenta między szpitalami.
def transfer(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('appointments_app:information', args=()))


# Widok renderuje HTML dla badań.
def tests(request, pat_id):
    p = Patient.objects.get(id=pat_id)
    t = Test.objects.filter(patient=p)
    context = {'patient': p,
               'test': t}
    return render(request, 'appointments_app/tests.html', context)


# Widok renderuje HTML dla tworzenia na nowych badań
def createTest(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'appointments_app/createTest.html', context)


# Moduł zajmuje się tworzeniem obiektu badań w bazie danych.
# Po utworzeniu badania, użytkownik jest przekierowany do karty badań.
def createTestInfo(request, pat_id):
    global uname
    name = (request.POST['name'])
    t = Test.objects.create()
    description = (request.POST['description'])
    try:
        if request.FILES['file']:
            file = request.FILES['file']
    except MultiValueDictKeyError:
        placeholder = ""
        t.testResults = placeholder
    else:
        t.testResults = file
    patient = Patient.objects.get(id=pat_id)
    doctor = Doctor.objects.get(username=uname)
    t.name = name
    t.description = description

    t.doctor = doctor
    t.patient = patient
    t.save()

    activity = f'Doctor {doctor.username} created a new test for Patient {patient.username} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)

    return HttpResponseRedirect(reverse('appointments_app:tests', args=pat_id))


# Moduł zajmuje się publikowaniem nieopublikowanego badania. Użytkownik jest przenoszony do strony z badaniami
def releaseTest(request, test_id):
    t = Test.objects.get(id=test_id)
    t.released = True
    t.save()

    activity = f'Patient {t.patient.username}\'s test results were released by Doctor' \
        f' {t.doctor.username} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)

    return HttpResponseRedirect(reverse('appointments_app:tests', args=(t.patient.id,)))


# moduł wyświetlania zawartości badania dla pacjenta
def testDetails(request, test_id):
    global uname
    test = Test.objects.get(id=test_id)
    context = {'test': test}
    return render(request, 'appointments_app/testDetails.html', context)


# widok zajmuje się renderowaniem HTMLa dla umawiania wizyt.
def appointments(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # pielęgniarka może utworzyć albo zaktualizować wizytę u Doktora w lokalizacj, w której pracuje
                # pielęgniarka nie może anulować wizyt.
                appointments = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appointments,
                           'employee': n,
                           'type': utype}
                return render(request, 'appointments_app/appointments.html', context)
        else:
            utype = "Doctor"
            # Doktor może utworzyć albo zaktualizować wizytę u Doktora w lokalizacj, w której pracuje
            # Doktor może anulować wizyte.
            appointments = Appointment.objects.filter(location=d.workplace)
            this_appointments = Appointment.objects.filter(doctor=d)
            context = {'appointments': appointments,
                       'this_appointments': this_appointments,
                       'employee': d,
                       'type': utype}
            return render(request, 'appointments_app/appointments.html', context)
    else:
        utype = "Patient"
        # Pacjent może utworzyć wizytę z jakimkolwiek doktorem
        # Pacjent może aktualizować SWOJĄ wizytę
        # Pacjent może anulować SWOJĄ wizytę
        appointments = Appointment.objects.filter(patient=p)
        context = {'appointments': appointments,
                   'user': p,
                   'type': utype}
        return render(request, 'appointments_app/appointments.html', context)


# Widok odpowiadający za renderowanie HTMLa dla umawiania wizyt.
def createAppointment(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create an appointment with any patient and any Doctor from their workplace.
                patients = Patient.objects.order_by("-lastName")
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'patients': patients,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'appointments_app/createAppointment.html', context)
        else:
            utype = "Doctor"
            # Doctors can create an appointment with any patient with themselves.
            patients = Patient.objects.order_by("-lastName")
            context = {'patients': patients,
                       'doctor': d,
                       'type': utype}
            return render(request, 'appointments_app/createAppointment.html', context)
    else:
        utype = "Patient"
        # Patients can create an appointment with any Doctor
        doctors = Doctor.objects.order_by("-lastName")
        context = {'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'appointments_app/createAppointment.html', context)


# This module handles creating a database object for an appointment after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the appointments screen.
def createAppointmentInfo(request):
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year,
                                              phase=phase)
    except Appointment.DoesNotExist:
        hp = Appointment.objects.create()
        hp.patient = patient
        hp.doctor = doctor
        hp.month = month
        hp.day = day
        hp.year = year
        hp.appttime = appttime
        hp.phase = phase
        hp.location = location
        hp.save()

        activity = f'User {uname} created an appointment at {location.name} on ' \
            f'{month},{day},{year} {appttime} {phase} - logged on: ' \
            f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
        logActivity(activity)
        return HttpResponseRedirect(reverse('appointments_app:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'appointments_app/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can create an appointment with any patient and any Doctor from their workplace.
                    patients = Patient.objects.order_by("-lastName")
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'patients': patients,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'appointments_app/createAppointment.html', context)
            else:
                utype = "Doctor"
                # Doctors can create an appointment with any patient with themselves.
                patients = Patient.objects.order_by("-lastName")
                context = {'patients': patients,
                           'doctor': d,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'appointments_app/createAppointment.html', context)
        else:
            utype = "Patient"
            # Patients can create an appointment with any Doctor
            doctors = Doctor.objects.order_by("-lastName")
            context = {'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'appointments_app/createAppointment.html', context)


# This module simply renders the HTML page for the update appointment screen.
def updateAppointment(request, appt_id):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'appointments_app/updateAppointment.html', context)
        else:
            utype = "Doctor"
            # Doctors can update an appointment to be with any Doctor from their workplace
            appointment = Appointment.objects.get(id=appt_id)
            patient = appointment.patient
            doctors = Doctor.objects.filter(workplace=d.workplace)
            context = {'appointment': appointment,
                       'patient': patient,
                       'doctors': doctors,
                       'type': utype}
            return render(request, 'appointments_app/updateAppointment.html', context)
    else:
        utype = "Patient"
        # Patients can update an appointment to be with any Doctor
        appointment = Appointment.objects.get(id=appt_id)
        doctors = Doctor.objects.order_by("-lastName")
        context = {'appointment': appointment,
                   'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'appointments_app/updateAppointment.html', context)


# This module handles modifying the database object for an appointment after retrieving POST data from the form
# submission. After the object is updated and saved, the user is redirected to their appointments screen.
def updateAppointmentInfo(request, appt_id):
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year,
                                              phase=phase)
    except Appointment.DoesNotExist:
        appt = Appointment.objects.get(id=appt_id)
        appt.doctor = doctor
        appt.month = month
        appt.day = day
        appt.year = year
        appt.appttime = appttime
        appt.phase = phase
        appt.location = location
        appt.save()

        activity = f'User {uname} updated Appointment #{appt_id} - logged on: ' \
            f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
        logActivity(activity)
        return HttpResponseRedirect(reverse('appointments_app:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'appointments_app/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can update an appointment to be with any Doctor from their workplace
                    appointment = Appointment.objects.get(id=appt_id)
                    patient = appointment.patient
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'appointment': appointment,
                               'patient': patient,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'appointments_app/updateAppointment.html', context)
            else:
                utype = "Doctor"
                # Doctors can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=d.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'appointments_app/updateAppointment.html', context)
        else:
            utype = "Patient"
            # Patients can update an appointment to be with any Doctor
            appointment = Appointment.objects.get(id=appt_id)
            doctors = Doctor.objects.order_by("-lastName")
            context = {'appointment': appointment,
                       'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'appointments_app/updateAppointment.html', context)


# This module handles deleting the database object for an appointment. Afterwards, the user is redirected to
# their appointments screen.
def cancelAppointment(request, appt_id):
    Appointment.objects.get(id=appt_id).delete()

    activity = f'User {uname} cancelled Appointment #{appt_id} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:appointments', args=()))


# This module simply loads the HTML page for the prescriptions screen.
def prescriptions(request):
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                pres = Prescription.objects.filter(patient__hospital=n.workplace)
                context = {'prescriptions': pres,
                           'type': utype,
                           'employee': n}
                return render(request, 'appointments_app/prescriptions.html', context)
        else:
            pres = Prescription.objects.filter(doctor=d)
            presatw = Prescription.objects.filter(patient__hospital=d.workplace)
            utype = "Doctor"
            context = {'prescriptions': pres,
                       'presatw': presatw,
                       'type': utype,
                       'employee': d}
            return render(request, 'appointments_app/prescriptions.html', context)
    else:
        utype = "Patient"
        pres = Prescription.objects.filter(patient=p)
        context = {'prescriptions': pres,
                   'type': utype,
                   'patient': p}
        return render(request, 'appointments_app/prescriptions.html', context)


# This module simply renders the HTML page for the create prescription screen.
def createPrescriptions(request):
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients}
    return render(request, 'appointments_app/createPrescriptions.html', context)


# This module handles creating a database object for a prescription after retrieving POST data from the form submission.
#  After the object is created and saved, the user is redirected to the prescriptions screen.
def createPrescriptionsInfo(request):
    global uname
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.create()
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()

    activity = f'Doctor {doctor.username} created a prescription for Patient {patient.username} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:prescriptions', args=()))


# This module simply renders the HTML page for the update prescriptions screen.
def updatePrescriptions(request, pres_id):
    p = Prescription.objects.get(id=pres_id)
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients,
               'prescription': p}
    return render(request, 'appointments_app/updatePrescriptions.html', context)


# This module handles modifying the database object after retrieving POST data from the form submission.
# After the object is updated and saved, the doctor is redirected to their prescriptions screen.
def updatePrescriptionsInfo(request, pres_id):
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.get(id=pres_id)
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()

    activity = f'Doctor {doctor.username} updated Prescription #{pres_id} ' \
        f'for Patient {patient.username} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:prescriptions', args=()))


# This module handles deleting the database object for a prescription. Afterwards, the doctor is redirected to
# their prescriptions screen.
def removePrescriptions(request, pres_id):
    Prescription.objects.get(id=pres_id).delete()

    activity = f'Doctor {uname} removed Prescription #{pres_id} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:prescriptions', args=()))


# This module simply renders the HTML page for the calendar screen.
def calendar(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'appointments_app/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can view all appointments for the day and week between patients and doctors, in their workplace
                appts = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appts,
                           'user': n,
                           'type': utype}
                return render(request, 'appointments_app/calendar.html', context)
        else:
            utype = "Doctor"
            # Doctors can view all of their appointments on the calendar
            appts = Appointment.objects.filter(doctor=d)
            context = {'appointments': appts,
                       'user': d,
                       'type': utype}
            return render(request, 'appointments_app/calendar.html', context)
    else:
        utype = "Patient"
        # Patients can view all of their appointments on the calendar
        appts = Appointment.objects.filter(patient=p)
        context = {'appointments': appts,
                   'user': p,
                   'type': utype}
        return render(request, 'appointments_app/calendar.html', context)


# This module simply renders the activity log for an administrator account
def log(request):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\appointments_app\\log\\" + filename, 'r')
    appString = target.readline()
    logString = []
    while appString != "":
        logString.append(appString)
        appString = target.readline()
    target.close()
    context = {'logString': logString}
    return render(request, 'appointments_app/log.html', context)


# This module simply renders the statistics page for an administrator account
def statistics(request):
    admins = Administrator.objects.count()
    doctors = Doctor.objects.count()
    nurses = Nurse.objects.count()
    patients = Patient.objects.count()
    appts = Appointment.objects.count()
    pres = Prescription.objects.count()
    context = {'admins': admins,
               'doctors': doctors,
               'nurses': nurses,
               'patients': patients,
               'appointments': appts,
               'prescriptions': pres}
    return render(request, 'appointments_app/statistics.html', context)


# This module simply renders the main messaging page for a user. All of their received and sent message are displayed
# on the page, with various options for the user to choose from.
def messages(request):
    global uname
    try:
        m = Message.objects.filter(receiverDelete=False)
        mess = m.filter(receiverName=uname)
    except Message.DoesNotExist:
        mess = Null
    try:
        sm = Message.objects.filter(senderDelete=False)
        sendmess = sm.filter(senderName=uname)
    except Message.DoesNotExist:
        sendmess = Null
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    context = {'messages': mess,
               'type': utype,
               'sendMessages': sendmess}
    return render(request, 'appointments_app/messages.html', context)


# This module simply renders the create message page for a user.
def createMessages(request):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins}
    return render(request, 'appointments_app/createMessages.html', context)


# This module simply renders the reply message page for a user.
def replyMessages(request, mess_id):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins,
               'message': Message.objects.get(id=mess_id)}
    return render(request, 'appointments_app/replyMessages.html', context)


# This module handles creating a database object for a message after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main messages page.
def createMessagesInfo(request, mess_id):
    global uname
    subject = (request.POST['subject'])
    description = (request.POST['message'])
    m = Message.objects.create()
    if mess_id != "-1":
        replyMess = Message.objects.get(id=mess_id)
        if replyMess.senderName == uname:
            m.receiverName = replyMess.receiverName
            m.subjectLine = "RE - " + subject
        else:
            m.receiverName = replyMess.senderName
            m.subjectLine = "RE - " + subject
    else:
        username = LogInInfo.objects.get(id=(request.POST['users'])).username
        m.receiverName = username
        m.subjectLine = subject
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
                    return render(request, 'appointments_app/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    m.senderName = uname
    m.senderType = utype
    m.date = date.today()
    m.message = description
    m.save()

    activity = f'{utype} {uname} sent a message to {m.receiverName} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return messages(request)


# This module simply displays the View Message page for a user when they select the option to view a received/sent
# message.
def viewMessages(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    context = {'message': mess}
    return render(request, 'appointments_app/viewMessages.html', context)


# This module handles deleting a preexisting message from a user's inbox.
def deleteMessages(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    if uname == mess.senderName:
        mess.senderDelete = True
        mess.save()
    else:
        mess.receiverDelete = True
        mess.save()

    if mess.senderDelete is True and mess.receiverDelete is True:
        mess.delete()

    activity = f'{uname} deleted message #{mess_id} - logged on: ' \
        f'{datetime.datetime.now().strftime("%m/%d/%y @ %H:%M:%S")}'
    logActivity(activity)
    return HttpResponseRedirect(reverse('appointments_app:messages', args=()))

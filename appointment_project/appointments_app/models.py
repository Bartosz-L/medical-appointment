from django.db import models
from datetime import date


# Create your models here.

# defnicja pól w modelu Szpital
class Hospital(models.Model):
    name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


# definicja pół modelu Kontakt w Nagłych Przypadkach
class EmergencyContact(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.firstName} {self.lastName}'


# definicja pól w modelu Pacjent
class Patient(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceId = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True, on_delete=models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    username = models.CharField(max_length=30, default='')
    hospital = models.ForeignKey(Hospital, default=None, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    # metoda pobierająca kontakt w nagłych przypadkach dla danego pacjenta
    def getEmergencyContact(self, patient):
        return patient.contact

    # metoda pobierająca dane szpitala, w którym leczy się pacjent
    def getHospital(self, patient):
        return patient.hospital


# definicja pól modelu Doktor
class Doctor(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def getWorkplace(self, doctor):
        return doctor.workplace


# definicja pól dla modelu Pielęgniarka
class Nurse(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def getWorkplace(self, nurse):
        return nurse.workplace


# definicja pól modelu Admin
class Administrator(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def getWorkplace(self, admin):
        return admin.workplace


# definicja pól modelu Recepty
class Prescription(models.Model):
    name = models.CharField(max_length=50, default='')
    patient = models.ForeignKey(Patient, null=True, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.PROTECT)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def getPatient(self, prescription):
        return prescription.patient

    def getDoctor(self, prescription):
        return prescription.doctor


# definicja pół modelu Badania
class Test(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500)
    released = models.BooleanField(default=False)
    testResults = models.FileField(upload_to='tests', null=True, blank=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def getPatient(self, test):
        return test.patient

    def getDoctor(self, test):
        return test.doctor


# definicja pól modelu Wizyty
class Appointment(models.Model):
    month = models.CharField(max_length=2, default='')  # '12'
    day = models.CharField(max_length=2, default='')  # '01'
    year = models.CharField(max_length=4, default='')  # '2019'
    appointmentTime = models.CharField(max_length=5, default='')  # '05:30'
    phase = models.CharField(max_length=2, default='')  # 'AM' or 'PM'
    patient = models.ForeignKey(Patient, null=True, on_delete=models.PROTECT)
    location = models.ForeignKey(Hospital, null=True, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.PROTECT)

    def getPatient(self, appointment):
        return appointment.patient

    def getLocation(self, appointment):
        return appointment.location

    def getDoctor(self, appoint):
        return appoint.doctor


# definicja pól modelu Wiadomość
class Message(models.Model):
    senderName = models.CharField(max_length=50, default='')
    senderType = models.CharField(max_length=50, default='')
    receiverName = models.CharField(max_length=50, default='')
    viewed = models.BooleanField(default=False)
    date = models.DateField(default=date.today())
    subjectLine = models.CharField(max_length=50, default='')
    message = models.TextField(max_length=500, default='')
    senderDelete = models.BooleanField(default=False)
    receiverDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.subjectLine

    def getSenderType(self, message):
        return message.senderType


# definicja pól dla modelu LogIn
class LogInInfo(models.Model):
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.username

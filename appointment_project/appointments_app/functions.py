# imports
from .models import Patient
from .models import Doctor
from .models import Nurse
from .models import Administrator


def getUserType(uname):
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
                    utype = ''
                else:
                    utype = "Administrator"

            else:
                utype = "Nurse"
        else:
            utype = "Doctor"

    else:
        utype = "Patient"
    return utype

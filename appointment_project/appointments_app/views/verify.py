from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from ..models import LogInInfo
from .logActivity import logActivity

uname = ''


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

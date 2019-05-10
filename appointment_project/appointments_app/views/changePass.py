from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from ..models import LogInInfo
from .logActivity import logActivity


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

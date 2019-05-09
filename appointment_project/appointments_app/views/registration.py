from django.shortcuts import render


# Widok odpowiada za renderowanie HTMLa dla strony do rejestracji
def registration(request):
    return render(request, 'appointments_app/registration.html')

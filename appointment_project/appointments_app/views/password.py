from django.shortcuts import render


# widok renderuje HTML dla zmiany hasła
def password(request):
    return render(request, 'appointments_app/password.html')

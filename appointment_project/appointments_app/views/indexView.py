from django.views.generic.list import ListView
from ..models import LogInInfo


# Widok odpowiada za generyczny templete view dla strony index,
# do której użytkownik będzie się logował, bądź rejestrował, jeżeli nie posiada konta
class IndexView(ListView):
    template_name = 'appointments_app/index.html'
    context_object_name = 'user_login_information'

    def get_queryset(self):
        return LogInInfo.objects.order_by('-username')

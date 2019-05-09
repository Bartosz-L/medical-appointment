from django.urls import path
from . import views

app_name = 'appointments_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('verify/', views.verify, name="verify"),
]

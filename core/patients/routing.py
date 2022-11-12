from django.urls import path
from patients.consumer import *

ws_urlpatterns = [
    path('ws/appointment/',AppointmentConsumer.as_asgi()),
]
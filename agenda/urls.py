from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendario_publico, name="calendario"),
    path("staff/", views.calendario_staff, name="staff_calendario"),
    path("staff/reservar/", views.reservar, name="reservar"),
    path("staff/cancelar/<int:appt_id>/", views.cancelar, name="cancelar"),
]

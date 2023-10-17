from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    #API
    path("api/", views.api_reservation, name='reservations'),
    path("api/<int:id>/out/", views.reservation_out),
    path("api/<int:id>/pay/", views.reservation_pay),
    path("api/<str:plate>/", views.reservation_details, name="plate"),

    #Parking
    path("", views.reservation, name='reservations'),

    #Auxiliares
    path("list/reservations/", views.reservations, name='reservations')

]
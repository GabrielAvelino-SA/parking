from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    #API
    path("api/", views.api_reservation, name='reservations'),
    path("api/<int:id>/out/", views.api_out),
    path("api/<str:plate>/pay/", views.api_payment),
    path("api/<str:plate>/", views.reservation_details, name="plate"),

    #Parking
    path("", views.reservation_home, name='reservations'),
    path("pay/",views.payment, name="payment"),
    path("<str:plate>/out/",views.checkOut, name="checkOut"),
    path("api/<str:plate>/", views.reservation_details, name="plate"),

    #Auxiliares
    path("list/reservations/", views.reservations, name='reservations')

]
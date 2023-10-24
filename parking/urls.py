from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    #API        
    path("api/", views.api_reservation, name='reservations'),
    path("api/list/", views.reservations),
    path("api/<str:plate>/pay/", views.api_payment),
    path("api/<str:plate>/out/", views.api_out),
    path("api/<str:plate>/", views.reservation_details, name="plate"),

    #Parking
    path("", views.reservation),
    path("pay/",views.payment),
    path("out/",views.checkOut),
]
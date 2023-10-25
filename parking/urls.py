from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    #API        
    path("api/", views.api_reservation, name='reservations'),
    path("api/list/", views.api_reservations),
    path("api/<str:plate>/", views.api_reservation_detail),
    path("api/<str:plate>/pay/", views.api_payment),
    path("api/<str:plate>/out/", views.api_out),

    #Parking
    path("", views.reservation),
    path("pay/",views.payment),
    path("out/",views.checkOut),
    path("list/", views.list_reservation), 
    path("<str:plate>/", views.reservation_detail, name="plate"),   
]
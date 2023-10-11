from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    #API
    path("", views.new_reservation, name='reservations'),
    path("<int:id>/out/", views.reservation_out),
    path("<int:id>/pay/", views.reservation_pay),
    path("<str:plate>/", views.reservation_details, name="plate"),    


    #Auxiliares 
    path("list/reservations/", views.reservations, name='reservations')

]
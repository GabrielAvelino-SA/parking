from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("parking/", views.parking, name='parking'),
    path("parking/<str:plate>/", views.plate_detail, name="plate"), #VALIDAR placa String    
    path("parking/<int:id>/out/", views.reservation_out, name="out"),
    #path("parking/<int:id>/pay/", views.id_pay, name="id_pay"),

]
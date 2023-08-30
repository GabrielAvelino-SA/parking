from django.contrib import admin
from django.urls import include ,path
from . import views

urlpatterns = [
    path("",views.reservation, name="reservation"),
    path("<id>/out/", views.id_out, name="id_out"),
    path("<id>/pay/", views.id_pay, name="id_pay"),
    path("<plate>/", views.plate, name="plate"),
    
]
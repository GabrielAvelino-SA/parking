from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("parking/<str:plate>/", views.plate_detail, name="plate"),
    path("parking/", views.parking, name='parking'),

    path("parking/<int:id>/", views.parking_detail, name="reservation"),
    
    #path("parking/<int:id>/out/", views.id_out, name="id_out"),
    #path("parking/<int:id>/pay/", views.id_pay, name="id_pay"),
    #path("parking/<str:plate>/", views.parking_detail, name="plate"),

]
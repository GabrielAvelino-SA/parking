from django.contrib import admin
from django.urls import include ,path
from . import views

urlpatterns = [
    path("",views.reservation, name="reservation"),
    #path("<id>/", views.id_, name="id_"),
    
]
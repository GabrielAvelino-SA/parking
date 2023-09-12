from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    path("parking/", views.parking, name='parking'),
    path("parking/<str:plate>/", views.plate_detail, name="plate"),
    path("parking/<int:id>/out/", views.ReservationView.as_view()),
    #path("parking/<int:id>/pay/", views.reservation_pay, name="id_pay"),

]
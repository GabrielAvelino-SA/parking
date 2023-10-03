from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    path("", views.reservations, name='reservations'),
    path("newUser/",views.new_user, name="New"),
    path("<int:id>/", views.reservation),
    #path("<str:plate>/", views.reservation, name="plate"),
    path("<int:id>/out/", views.reservation_out),
    path("<int:id>/pay/", views.reservation_pay),

]
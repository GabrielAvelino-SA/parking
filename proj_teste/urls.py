
from django.contrib import admin
from django.urls import path,include
from parking.views import ReservationViewSet
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'register', ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include(router.urls)),
    
    #My URLS
    path('', include("parking.urls")),
]
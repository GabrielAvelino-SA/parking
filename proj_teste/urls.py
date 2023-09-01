
from django.contrib import admin
from django.urls import path,include
from parking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('parking/', include("parking.urls"))
]
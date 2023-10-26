from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #My URLS
    path('parking/', include("parking.urls")),

]

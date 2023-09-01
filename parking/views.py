from django.shortcuts import render
from django.http import HttpResponse
#My
from rest_framework import viewsets
from .models import Reservation
from .serializers import ReservationSerializer


# my views here.

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

def reservation(request,pk):
   
    if request.method == 'POST':
        return HttpResponse('post')
    
    else:
        return HttpResponse('None')

def id_out(request, id):
    out = request.get()
    pass
def id_pay(request, id):
    pass
def plate(requeest):
    pass
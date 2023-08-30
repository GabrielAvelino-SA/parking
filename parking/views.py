from django.shortcuts import render
from django.http import HttpResponse
from parking.models import Reservation
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# my views here.
def reservation(request):
    if request.method == 'GET':
        get_ = request.get()
        return HttpResponse(get_)
    
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
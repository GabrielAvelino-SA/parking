from django.shortcuts import render
from django.http import HttpResponse
from parking.models import Reservation
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from parking.models import Reservation

# my views here.

@api_view(['GET', 'POST'])
def reservation(request,pk):

    try :
        reservation = Reservation.objects.get(pk=id)
    except:
        return HttpResponse('notFound')
    if request.method == 'GET':
        get_ = serializers.serialize("json", Reservation.objects.all())
        
        return HttpResponse(len(get_))
    
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
from rest_framework.decorators import api_view

from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render
from parking.models import Reservation,Historico
from datetime import datetime, timedelta
from re import search
from django.core.exceptions import ValidationError

#Detail reservatios

@api_view(['GET'])
def reservations(request):
    reservations = Reservation.objects.all()
    if reservations:
         #reservas ateriores
         return render(request, "parkinListDetail.html", {"reservations":reservations})
    else:
        return HttpResponse(status=404)

@api_view(['GET'])
def reservation(request,id):    
    if Reservation.objects.filter(pk=id).exists():
        query = Reservation.objects.get(pk=id)
        return render (request, "reservationDetail.html", {"reservation":query})
    else:
        return HttpResponse("Reserva Não encrontrada")

@api_view(['POST'])
def new_user(request):
    plate = request.data['plate']
    #Regex validação mercosul
    def Validateplate(plate):
        return search("^[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}",plate)
    
    if Validateplate(plate):
        if Reservation.objects.filter(plate=request.data['plate']).exists():
            reservation = Reservation.objects.get(plate=request.data['plate'])
            if reservation.left:
                reservation.paid = bool(False)
                reservation.left = bool(False)
                reservation.date = datetime.now()
                reservation.save()

                Historico.objects.create(
                    checkIn = datetime.now(), 
                    id_reservation = reservation
                )
                #criarnovo checkIn
                return render(request, "CheckIn/newCheckIn.html")
            else:
                return HttpResponse("Há uma reserva em aberto para estes dados", status=201)
        else:
            newUser = Reservation.objects.create(plate=plate)
            Historico.objects.create(
                checkIn = datetime.now(), 
                id_reservation = newUser
                )
            return HttpResponse(f"The Plate {plate} is valid, your number check in is {newUser.pk}")
        
    else:
        return HttpResponse(f"The Plate {plate} is not valid", status=201)
    
@api_view(['PUT'])
def reservation_out(request,id):
        
        if Reservation.objects.filter(id=id).exists():
            reservation = Reservation.objects.get(id=id)
            historico = Historico.objects.filter(id_reservation = id)[:1]

            #pagamento realizado/não realizou checkout
            if reservation.left:
                return render(request, "CheckOut/alreadyCheckOut.html")
            if not reservation.paid:
                return render(request,'CheckIn/notPayment.html')
            elif not reservation.left:
                status = request.data['left']
                reservation.left = bool(status)
                reservation.save()
                #condicional de validação
                if status:
                    for object in historico:
                        object.checkOut = datetime.now()
                        object.save()
                return render(request, "CheckOut/successCheckOut.html")
        else:
            return HttpResponse(status=404)

@api_view(['PUT'])
def reservation_pay(request,id):
     
     if Reservation.objects.filter(id=id).exists:
          reservation = Reservation.objects.get(id=id)
          if reservation.paid:
            return render(request,'CheckIn/alreadyPayment.html')
          status = request.data['paid']
          reservation.paid = bool(status)
          reservation.save()
          return render(request,'CheckIn/successPayment.html')
     else:
        return HttpResponse(status=404)
     
@api_view(['GET'])
def historico(request, id):
    history = Historico.objects.filter(id_reservation=id)
    if historico:
         return render(request, "Historico/listHistory.html", {"history":history})
    else:
        return HttpResponse(status=404)


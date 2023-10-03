from rest_framework.decorators import api_view

from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render
from parking.models import Reservation,Historico
from datetime import datetime, timedelta
from re import search
from django.core.exceptions import ValidationError

#Detail reservatios

class ReservationDetail(generic.ListView):
    queryset = Reservation.objects.all()


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
        return HttpResponse("Objeto Não encontrado")
#New Reservation
@api_view(['POST'])
def new_user(request):
    plate = request.data['plate']
    def Validateplate(plate):
        return search("^[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}",plate)
    
    if Validateplate(plate):
        if Reservation.objects.filter(plate=request.data['plate']).exists():
            reservation = Reservation.objects.get(plate=request.data['plate'])
            #se usuario não fez checkout
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
                pass
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
        reservation =  Reservation.objects.get(id=id)
        if reservation.paid and reservation.left == False:
            status = request.data['left']
            reservation.left = bool(status)
            reservation.save()
            return HttpResponse("Success Check Out", status=201)
        elif reservation.left:
            return HttpResponse("Realizar nova entrada <button type=\"button\">Click Me!</button>")
        elif reservation.paid == False:
            return HttpResponse("Realizar pagamento? <button type=\"button\">Click Me!</button>", status=201)#se sim dar entrada ao pagamento
        else:
            return HttpResponse(status=404)

@api_view(['PUT'])
def reservation_pay(request,id):
     reservation = Reservation.objects.get(id=id)
     if reservation:
          if reservation.paid:
            return HttpResponse("Pagamento já Realizado", status=201)
          status = request.data['paid']
          reservation.paid = bool(status)
          reservation.save()
          return HttpResponse("Pagamento Realizado", status=201)
     else:
        return HttpResponse(status=404)
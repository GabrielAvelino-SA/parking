from rest_framework.decorators import api_view
from rest_framework import serializers

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import generic
from django.shortcuts import render
from django.core.validators import RegexValidator
from parking.models import Reservation,Historico
from datetime import datetime

#Detail reservatios

class ReservationDetail(generic.ListView):
    queryset = Reservation.objects.all()


@api_view(['GET'])
def parking_detail(request):
    reservations = Reservation.objects.all()
    if reservations:
         #reservas ateriores
         return render(request, "parkinListDetail.html", {"reservations":reservations})
    else:
        return HttpResponse(status=404)

@api_view(['GET'])
def reservation(request,id):
    if Reservation.objects.filter(pk=id).exists:
        query = Reservation.objects.get(pk=id)
        return 
    else:
        return HttpResponse("Não encontrado")

#New Reservation
@api_view(['POST'])
def parking(request):
    if Reservation.objects.filter(plate=request.data['plate']).exists():
        reservation = Reservation.objects.get(plate=request.data['plate'])
    else:
        reservation = None

    if reservation and reservation.left == False:
        return HttpResponse("Há uma reserva em aberto para estes dados", status=201)
    else:

        historico = Historico()
        historico.time = '00:00:00'
        #historico.id_reservation = 
        query = HistorySerializer(data=queryHistorico.date, date=True)
        if query.is_valid:
            queryHistorico.save()
        else:
            return JsonResponse(queryHistorico.errors, status=406)

    try:
        # Novo Checkout
        if Reservation.objects.filter(plate=request.data['plate']).exists():
            queryReservation = Reservation.objects.get(plate=request.data['plate'])
        else:
            queryReservation = None

        if queryReservation and queryReservation.left == False:
            return HttpResponse("Há uma reserva em aberto para estes dados", status=201)
        
        queryHistorico = Historico()
        queryHistorico.time = '00:00:00'
        query = HistorySerializer(data=queryHistorico.date, date=True)

        if query.is_valid:
            queryHistorico.save()
        else:
            return JsonResponse(queryHistorico.errors, status=406)
    
        queryReservation.time = datetime.now().time()
        queryReservation.left = bool(False)
        queryReservation.paid = bool(False)

        queryReservation.save()
        return HttpResponse("Check-In Realizado", status=201)
    
    except:
        # cadastro e checkout
        reservation = ReservationSerializer(data=request.data, partial=True)
        if reservation.is_valid():
            reservation.save()

            history = HistorySerializer(partial=True)
            history.id_reservation = reservation.id
            
            history.save()
            return HttpResponse("Check-In Realizado", status=201)
        else:
            return JsonResponse(reservation.errors, status=406)

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
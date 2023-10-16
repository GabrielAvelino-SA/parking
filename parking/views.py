from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.core.exceptions import ValidationError
from datetime import datetime
from re import search

from parking.models import Reservation, Historico
from parking.forms import FormReservation

# API
def new_reservation(plate):

    try:
        reserva = Reservation(plate=plate)
        reserva.full_clean()
    except ValidationError:
        return {'message':f'The Plate { plate } not valid'}


    if Reservation.objects.filter(plate=plate).exists():
        reservation = Reservation.objects.get(plate=plate)
        
        if reservation.left:
            reservation.paid = bool(False)
            reservation.left = bool(False)
            reservation.date = datetime.now()
            reservation.save()

            Historico.objects.create(
                checkIn = datetime.now(), 
                id_reservation = reservation
            )

            return {'message':f'The Plate { plate } is valid, your number check in is {reservation.pk}'}
        else:
            return {'message':'Open reservation'}
    else:
        newUser = Reservation.objects.create(plate=plate)
        Historico.objects.create(
            checkIn = datetime.now(), 
            id_reservation = newUser
            )
        return {'message':f'The Plate { plate } is valid, your number check in is {newUser.pk}'}
    
# ----------- API -----------
@api_view(['POST'])
def api_reservation(request):
    new = new_reservation(request.data['plate'])
    return Response(new)
    
# ---------- Parking ---------
def reservation(request):
    validatedPlate = Validateplate(request.data['plate'])

    if validatedPlate:
        new = new_reservation(request.data['plate'])
        return render(request, )
    else:
        return Response({'message':f"The plate {request.data['plate']} is no Valid"})

@api_view(['PUT'])
def reservation_out(request,id):
        
        if Reservation.objects.filter(id=id).exists():
            reservation = Reservation.objects.get(id=id)
            historico = Historico.objects.filter(id_reservation = id).order_by("-id")[0]

            if reservation.left:
                return render(request, "Alert/warning.html",{'massage':'Check in Already Done'})
            if not reservation.paid:
                return render(request, "Alert/warning.html",{'massage':'You Need to Pay'})
            elif not reservation.left:
                status = request.data['left']
                reservation.left = bool(status)
                reservation.save()
                #condicional de validação
                if status:
                    historico.checkOut = datetime.now()
                    historico.save()

                return render(request, "Alert/success.html",{'massage':'Success Check Out'})
        else:
            return Response({"message":"Object inesisttete"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def reservation_pay(request,id):
     if Reservation.objects.filter(id=id).exists():

          reservation = Reservation.objects.get(id=id)
          status = request.data['paid']

          if reservation.paid:
            return render(request,'Alert/warning.html',{'massage':'Payment done'})
          elif status:
            reservation.paid = bool(status)
            reservation.save()
            return render(request,'Alert/success.html', {'massage':'Success Payment'})
          else:
              Response({'massage':'Invalid value'})
            #   return render(request,'Alert/warning.html', {'massage':'Invalid value'})
     else:
        return Response({"message":"Object inesisttete"}, status=400)

@api_view(['GET'])
def reservation_details(request,plate):
    if Reservation.objects.filter(plate=plate).exists():
        data = Historico.objects.select_related('id_reservation').filter(id_reservation__plate=plate ).values('checkIn','checkOut','id_reservation__plate')

        result = []
        for d in data:
            result.append({
                "checkIn": d['checkIn'],
                "checkOut": d['checkOut']
            })

        json = {
            'plate':data[0]['id_reservation__plate'],
            'hitory': result
            }
        return Response(json)
        # return render (request, "Reservation/reservationDetail.html", {'reservation':queryReservation,'history':queryHistory})
    else:
        return Response({"message":"Object inesisttete"}, status=status.HTTP_400_BAD_REQUEST)
        # return render(request, "Alert/warning.html", {'massage':'Reservation not found'})
    
#Auxiliares
@api_view(['GET'])
def reservations(request):
    if Reservation.objects.all().values():
         return Response(list(Reservation.objects.all().values()))
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    #render(request, "Auxiliares/reservationList.html", {"reservations":reservations})
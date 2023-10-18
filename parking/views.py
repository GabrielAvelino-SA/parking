from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.template import loader
from datetime import datetime

from parking.models import Reservation, Historico
from parking.forms import FormReservation


# ----------- API -----------

@api_view(['POST'])
def api_reservation(request):
    new = new_reservation(request.data['plate'])
    return Response(new)

@api_view(['PUT'])
def api_payment(request,id):
    payment = payment_reservation(id)   
    return Response(payment)

@api_view(['PUT'])
def api_out(request):
    payment = payment_reservation(id)
    return Response(payment)

# ---------- Parking ----

def reservation(request):   
        if request.method == 'POST':
            form = FormReservation(request.POST['plate'])
            if form.is_valid():                
                reservation = new_reservation(request.POST['plate'])
                return render(request, 'Alert/warning.html',{'message':reservation['message']})
            else:
                return render(request, "Alert/warning.html",{"message":f"The Plate '{request.POST['plate']}' is no Valid"}) 
        else:
            form = FormReservation("Reservation/newReservation.html")
        return render(request, 'Reservation/newReservation.html', {
        'form': form,
        })

def payment(request):
    if request.method == 'PUT':
        pass
    else:
        form = FormReservation(request.PUT)


# ------------ My Functions ------------
def new_reservation(plate):
    # Consulta reservas anteriores
    if Reservation.objects.filter(plate=plate).exists():
        reservation = Reservation.objects.get(plate=plate)
        # check In Realizado
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
        # retornar id separado
        return {'message':f'The Plate { plate } is valid, your number check in is {newUser.pk}'}
    
def payment_reservation(id):
     if Reservation.objects.filter(id=id).exists():
          reservation = Reservation.objects.get(id=id)
          if reservation.paid:
            return {'massage':'Payment done'}
          else:
            reservation.payment()
            return {'massage':'Success Payment'}
     else:
        return {"message":"Object inesisttete"}


def reservation_out(id):
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
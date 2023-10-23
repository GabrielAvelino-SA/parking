from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from datetime import datetime
from re import search   

from parking.models import Reservation, Historico
from parking.forms import FormReservation


# ----------- API -----------

@api_view(['POST'])
def api_reservation(request):
    if valiation_plate(request.data['plate']):
        return Response(new_reservation(request.data['plate']))
    return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def api_payment(request,plate):  
    return Response(payment = payment_reservation(plate) )

@api_view(['PUT'])
def api_out(request,plate):
    return Response(checkout_reservation(plate))

# ---------- Parking --------

def reservation(request):
    message  = ''
    if request.method == 'POST':
        if valiation_plate(request.POST['plate']):
            new = new_reservation(request.POST['plate'])
            form =  FormReservation("Reservation/Reservation.html")
            message = new['message']
        else:
            form = FormReservation("Reservation/Reservation.html")
            message = f"The Plate '{request.POST['plate']}' is no Valid"
    else:
        form = FormReservation("Reservation/ReservationHome.html")
    return render(request, 'Reservation/ReservationHome.html', {
    'form': form, 'message':message,    
    })

def payment(request):
    message = ''
    if request.method == 'POST':
        pay = payment_reservation(request.POST['plate'])
        form =  FormReservation(request.POST['plate'])
        message = pay['message']
    else:
        form = FormReservation("Reservation/payment.html")
    return render(request,'Reservation/payment.html',{
        'form':form, 'message':message      
        })
    
def checkOut(request):
    message = ''
    if request.method == 'POST':
        out  = checkout_reservation(request.POST['plate'])
        form =  FormReservation(request.POST['plate'])
        message = out['message']
        pass
    else:
        form = FormReservation("Reservation/checkOut.html")
    return render(request, "Reservation/checkOut.html",{
        'form':form, 'message':message
    })
        
# ------------ My Functions ------------

def valiation_plate(plate):
    return search("^[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}",plate)

def consulta_reservation(plate):
    if Reservation.objects.filter(plate=plate).exists():
        return Reservation.objects.get(plate=plate)
    return None

def new_reservation(plate):
    reservation = consulta_reservation(plate)
    if reservation:
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

def payment_reservation(plate):
     reservation = consulta_reservation(plate)
     if reservation:
          if reservation.paid:
            return {'message':'Payment done'}
          else:
            reservation.payment()
            return {'message':'Success Payment'}
     else:
        return {"message":"Object inesisttete"}

def checkout_reservation(plate):
        reservation = consulta_reservation(plate)
        if reservation:
            if reservation.left:
                return {'message':'Check in Already Done'}
            elif not reservation.paid:
                return {'message':'You Need to Pay'}
            else:
                reservation.checkout()
                # referenciar historico
                if status:
                    historico = Historico.objects.filter(id_reservation = reservation.pk).order_by("-id")[0]
                    historico.checkOut = datetime.now()
                    historico.save()
                return {'message':'CheckOut alread  '}
        else:
            return {"message":"Object inesisttete"}
        
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
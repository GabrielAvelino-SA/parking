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
    return Response({'message':f"plate '{request.data['plate']}' no valid"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def api_payment(request,plate):
    if not valiation_plate(plate):
        return Response(payment = payment_reservation(plate))
    return Response({'message':f"plate '{plate}' no valid"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def api_out(request,plate):
    return Response(checkout_reservation(plate))

# ---------- Parking --------

def reservation(request):
    message  = ''
    status = 200
    form = FormReservation("Reservation/ReservationHome.html")

    if request.method == 'POST':
        if not valiation_plate(request.POST['plate']):
            message = f"The Plate '{request.POST['plate']}' is no Valid"
            status = 400 
        else:       
            new = new_reservation(request.POST['plate'])
            message = new['message']
    else:
        status = 405

    return render(request, 
                  'Reservation/ReservationHome.html',
                  {'form': form, 'message':message}
                  ,status=status)

def payment(request):
    message = ''
    status = 200
    
    if request.method == 'POST':
        try:
            pay = payment_reservation(request.plate)
            form = FormReservation("Reservation/payment.html")
            message = pay['message']
        except None:
            status = 400
            form = FormReservation("Reservation/payment.html")
    else:
        status = 405
        form = FormReservation("Reservation/payment.html")

    return render(request,'Reservation/payment.html',{
        'form':form, 'message':message      
        },status = status)
    
def checkOut(request):
    message = ''
    status = 200
    if request.method == 'POST':
        out  = checkout_reservation(request.POST['plate'])
        form =  FormReservation(request.POST['plate'])
        message = out['message']
        pass
    else:
        status = 405
        form = FormReservation("Reservation/checkOut.html")
    return render(request, "Reservation/checkOut.html",{
        'form':form, 'message':message
    }, status=status)
        
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
            reservation.left = bool(False)
            reservation.left = bool(False)
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

def payment_reservation(plate):
    reservation = consulta_reservation(plate)
    if reservation:
          if reservation.paid:
            return {'message':'Payment done'}
          else:
            reservation.payment()
            return {'message':'Success Payment'}
    else:
        return None
     

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
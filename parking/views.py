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
    pay  = (payment_reservation(plate))
    if valiation_plate(plate) and pay:
       return Response(pay)            
    return Response({'message':f" The plate '{plate}' is invalid or nonexistent"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def api_out(request,plate):
    out = checkout_reservation(plate)
    if valiation_plate(plate) and out:
        return Response(out)
    return Response({'message':f" The plate '{plate}' is invalid or nonexistent"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_reservation_detail(request,plate):
    reservation = details_reservation(plate)
    if reservation:
        return Response(reservation)
    return Response({'message':f" The plate '{plate}' is invalid or nonexistent"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_reservations(request):
    if Reservation.objects.all().values():
         return Response(list(Reservation.objects.all().values()))
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ---------- Parking --------

def reservation(request):
    message  = ''
    status = 200
    form = FormReservation("Reservation/ReservationHome.html")
    if request.method == 'POST':
        if not valiation_plate(request.POST['plate']):
            message = f"The Plate '{request.POST['plate']}' is invalid"
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
        pay = payment_reservation(request.POST['plate'])
        form = FormReservation("Reservation/payment.html")
        if pay:
            message = pay['message']
        else:
            status = 400
            message = 'The plate is invalid or nonexistent'
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
        if out:
            message = out['message']
        else:
            status = 400
            message = 'The plate is invalid or no exist'
    else:
        status = 405
        form = FormReservation("Reservation/checkOut.html")
    return render(request, "Reservation/checkOut.html",{
        'form':form, 'message':message
    }, status=status)

def reservation_detail(request,plate):
    reservation = consulta_reservation(plate)
    if reservation:
        queryReservation = Reservation.objects.get(plate=plate)
        queryHistory = Historico.objects.filter(id_reservation=queryReservation.pk)
        return render (request, "Reservation/reservationDetail.html", {'reservation':queryReservation,'history':queryHistory})
    return render(request, {'message':f" The plate '{plate}' is invalid or nonexistent"}, status = status.HTTP_400_BAD_REQUEST)

def list_reservation(request):
    reservartions = Reservation.objects.all()
    return render(request,"Reservation/reservation.html",{'reservations':reservartions}, status = 200)

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
            return None
        
def details_reservation(plate):
    reservation = consulta_reservation(plate)
    if reservation:
        data = Historico.objects.select_related('id_reservation').filter(id_reservation__plate=plate ).values('checkIn','checkOut','id_reservation__plate')

        result = []
        for d in data:
            result.append({
                "checkIn": d['checkIn'],
                "checkOut": d['checkOut']
            })

        json = {
            'plate':data[0]['id_reservation__plate'],
            'history': result
            }
        return json
    else:
        return None

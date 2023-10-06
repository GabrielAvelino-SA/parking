from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import render
from parking.models import Reservation,Historico
from datetime import datetime
from re import search
#new Reservation
@api_view(['POST'])
def new_reservation(request):
    plate = request.data['plate']

    #Validação mercosul
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
                return render(request, "Alert/success.html", {'massage':f'The Plate { plate } is valid, your number check in is {reservation.pk}'})
            else:
                return render(request,'Alert/warning.html',{'massage':'Open reservation'})
        else:
            newUser = Reservation.objects.create(plate=plate)
            Historico.objects.create(
                checkIn = datetime.now(), 
                id_reservation = newUser
                )
            return render(request, "Alert/success.html", {'massage':f'The Plate { plate } is valid, your number check in is {newUser.pk}'})
    else:
        return render(request, "Alert/warning.html",{'massage':f"The plate {plate} is no Valid"})
  
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
            return HttpResponse(status=404)

@api_view(['PUT'])
def reservation_pay(request,id):
     if Reservation.objects.filter(id=id).exists:
          reservation = Reservation.objects.get(id=id)
          status = request.data['paid']

          if reservation.paid:
            return render(request,'Alert/warning.html',{'massage':'Payment done'})
          elif status:
            reservation.paid = bool(status)
            reservation.save()
            return render(request,'Alert/success.html', {'massage':'Success Payment'})
          else:
              return render(request,'Alert/warning.html', {'massage':'Invalid value'}) 
     else:
        return HttpResponse(status=404)

@api_view(['GET'])
def reservation_details(request,plate):
    if Reservation.objects.filter(plate=plate).exists():
        queryReservation = Reservation.objects.get(plate=plate)
        queryHistory = Historico.objects.filter(id_reservation=queryReservation.pk)
        return render (request, "Reservation/reservationDetail.html", {'reservation':queryReservation,'history':queryHistory})
    else:
        return render(request, "Alert/warning.html", {'massage':'Reservation not found'})

#Auxiliares
@api_view(['GET'])
def reservations(request):
    reservations = Reservation.objects.all()
    if reservations:
         #reservas ateriores
         return render(request, "Auxiliares/reservationList.html", {"reservations":reservations})
    else:
        return HttpResponse(status=404)
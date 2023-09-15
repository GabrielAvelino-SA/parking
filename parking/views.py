from rest_framework.decorators import api_view
from rest_framework import serializers

from django.http import HttpResponse, JsonResponse
from django.core.validators import RegexValidator
from parking.models import Reservation
from datetime import datetime

class ReservationSerializer(serializers.Serializer):
    id =  serializers.IntegerField(read_only=True)
    plate = serializers.CharField(
        max_length=8,
        read_only = False,
        validators=[
            RegexValidator(r"[A-Z]{3}[-][0-9][0-9A-J][0-9]{2}", 
            message="Wrong Format")]
        )
    time = serializers.TimeField(read_only=True)
    paid = serializers.BooleanField(default=False, read_only=True)
    left = serializers.BooleanField(default=False, read_only=True)

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)

class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    id_reservation = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    time = serializers.DurationField()
#Detail reservatios
@api_view(['GET'])
def plate_detail(request,plate):
    reservation = Reservation.objects.get(plate=plate)
    if reservation:
         #reservas aneriores
         return JsonResponse(ReservationSerializer(reservation).data, status=201)
    else:
        return HttpResponse(status=404)

#New Reservation
@api_view(['POST'])
def parking(request):
    try:
        # Novo Checkout
        query = Reservation.objects.get(plate=request.data['plate'])
        if query.left == False:
            return HttpResponse("Há uma reserva em aberto para estes dados", status=201)
        query.time = datetime.now().time
        query.paid = bool(False)
        query.paid = bool(False)
        query.save
        return HttpResponse("Check-In Realizado", status=201)
    except:
        # cadastro e checkout
        reservation = ReservationSerializer(data=request.data, partial=True)
        if reservation.is_valid():
            reservation.save()
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
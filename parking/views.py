#Rest Framework
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

from rest_framework import serializers
from django.core.validators import RegexValidator
from parking.models import Reservation


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

# my Views
@api_view(['POST'])
def parking(request):

    if request.method =='POST':
            data_ = JSONParser().parse(request)

            serializer = ReservationSerializer(data=data_, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def plate_detail(request,plate):
    
    reservation = Reservation.objects.get(plate=plate)
    if reservation:
         
        pass#Serializar api
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

@api_view(['PUT'])
def reservation_out(request,id):
    
        reservation =  Reservation.objects.get(id=id)
        if reservation:
             status = request.data['paid']
             reservation.paid = bool(status)
             reservation.save()
             return HttpResponse("ok",status=201)
        else:
            return HttpResponse(status=404)

@api_view(['PUT'])
def reservation_pay(request,id):
     
     reservation = Reservation.objects.get(id=id)
     if reservation:
          status = request.data['left']
          reservation.left = bool(status)
          reservation.save()
          return Response(status=201)
     else:
        return HttpResponse(status=404)
          
    
    
        
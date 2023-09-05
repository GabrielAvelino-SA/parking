from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import validators

#Rest Framework
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


#Modulos
from .models import Reservation
from .serializers import ReservationSerializer

# my Views

@api_view(['GET'])
def plate_detail(request,plate):

    try:
        reservation= Reservation.objects.get(plate=plate)

    except Reservation.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return JsonResponse(serializer.data)
    
    #TRY EXEPT FOR SECURITY


@api_view(['POST'])
def parking(request):
    if request.method =='POST':
            data = JSONParser().parse(request)
            #VALIDAR JSON
            serializer = ReservationSerializer(data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def parking_detail(request,id):
    try:
        reservation =  Reservation.objects.get(id=id)

    except Reservation.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method =='GET':
        serializer = ReservationSerializer(reservation)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReservationSerializer(reservation, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erros, status=400)
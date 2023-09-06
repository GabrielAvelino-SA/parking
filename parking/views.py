from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


#Rest Framework
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

#Modulos
from .models import Reservation
from .serializers import ReservationSerializer

# my Views
@api_view(['POST'])
def parking(request):

    if request.method =='POST':
            data = JSONParser().parse(request)
                   
            serializer = ReservationSerializer(data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            
            return JsonResponse(serializer.errors, status=406)
    else:
        return HttpResponse(status=405)

@api_view(['GET'])
def plate_detail(request,plate):

    try:
        reservation= Reservation.objects.get(plate=plate)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        
        serializer = ReservationSerializer(reservation)


        return JsonResponse(serializer.data)
    else:
        return HttpResponse(status=405)

@api_view(['PUT'])
def reservation_out(request,id):
    try:
        reservation =  Reservation.objects.get(id=id)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'PUT':
        data_ = JSONParser().parse(request)
        serializer = ReservationSerializer(reservation, data=data_)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(status=201)
        return JsonResponse(serializer.erros, status=406)
    else:
        return HttpResponse(staus=405)
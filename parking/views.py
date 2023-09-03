from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

#Rest Framework
from rest_framework.parsers import JSONParser    

#Modulos
from .models import Reservation
from .serializers import ReservationSerializer

# my Views

@csrf_exempt
def parking_list(request):
    if request.method == 'GET':
        parking = Reservation.objects.all()
        serializer = ReservationSerializer(parking,many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method =='POST':
            data =JSONParser().parse(request)
            serializer = ReservationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def parking_detail(request,plate):
    try:
        reservation =  Reservation.objects.get(plate=request.plate)

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

def id_out(request, id):
    out = request.get()
    pass
def id_pay(request, id):
    pass
def plate(requeest):
    pass


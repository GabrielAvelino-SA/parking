#Rest Framework
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

#Modulos
from .models import Reservation
from .serializers import ReservationSerializer

# my Views

class ReservationView(APIView): 
    '''
    update and update partial
    '''
    def put(self,request,id,format=None):

        try:
            querySet = Reservation.objects.get(id=id)
        except Reservation.DoesNotExist():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(querySet,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

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

    try:
        reservation= Reservation.objects.get(plate=plate)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        #serialização manual

        return Response(serializer.data)
    else:
        return Response(tatus=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def reservation_out(request,id):
    try:
        reservation =  Reservation.objects.get(id=id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        data_ = JSONParser().parse(request)
        serializer = ReservationSerializer(reservation, data=data_, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(serializer.erros, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(staus=status.HTTP_405_METHOD_NOT_ALLOWED)
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# my views here.
def reservation(request):
    #criate consulta

    data = { 'plate': 'FAA-1234' }
    return JsonResponse(data, status=200)
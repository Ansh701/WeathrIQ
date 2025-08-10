from django.shortcuts import render
from django.http import HttpResponse

def weather_view(request):
    return HttpResponse("<h1>WeathrIQ</h1>")

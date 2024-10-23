from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def login(request):
    return render(request, 'login.html')

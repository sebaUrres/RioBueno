from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def enfermero(request):
    return render(request, 'dashboardEnfermero.html')

def coordinador(request):
    return render(request, 'dashboardCoordinador.html')
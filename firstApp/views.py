from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def enfermero(request):
    return render(request, 'Dashboard-Enfermero.html')

def coordinador(request):
    return render(request, 'dashboardCoordinador.html')

def inventario(request):
    return render(request, 'inventario.html')

def dashinsumos(request):
    return render(request, 'dashboardinsumos.html')

def dashvisitas(request):
    return render(request, 'Dashboard-Visitas.html')

def detvisita(request):
    return render(request, 'Dashboard-DetallesV.html')

def regvisita(request):
    return render(request, 'Dashboard-RegistroV.html')

def pacientes(request):
    return render(request, 'Dashboard-Pacientes.html')
from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def enfermero(request):
    return render(request, 'enfermero/Dashboard-Enfermero.html')

def coordinador(request):
    return render(request, 'coordinador/dashboardCoordinador.html')

def inventario(request):
    return render(request, 'enfermero/inventario.html')

def dashinsumos(request):
    return render(request, 'enfermero/dashboardinsumos.html')

def dashvisitas(request):
    return render(request, 'enfermero/Dashboard-Visitas.html')

def detvisita(request):
    return render(request, 'enfermero/detallesVpaciente.html')

def regvisita(request):
    return render(request, 'enfermero/Dashboard-RegistroV.html')

def pacientes(request):
    return render(request, 'enfermero/Dashboard-Pacientes.html')

def ultimasV(request):
    return render(request, 'enfermero/ultimasvisitas.html')

def enfpedidos(request):
    return render(request, 'enfermero/pedirOmnic.html')
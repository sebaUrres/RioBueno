from django.shortcuts import render, redirect
from firstApp.models import *
from . import forms
from .forms import *

# Create your views here.

#enfermero
def login(request):
    return render(request, 'login.html')

def enfermero(request):
    return render(request, 'enfermero/Dashboard-Enfermero.html')

def inventario(request):
    return render(request, 'enfermero/inventario.html')

def dashinsumos(request):
    return render(request, 'enfermero/dashboardinsumos.html')

def dashvisitas(request):
    return render(request, 'enfermero/Dashboard-Visitas.html')

def detvisita(request):
    return render(request, 'enfermero/detallesVpaciente.html')

def regvisita(request):
    form = IngresoVisitaForms()  
    if request.method == 'POST':
        form = IngresoVisitaForms(request.POST)
        if form.is_valid():
            visita = form.save(commit=False) 
            visita.paciente_id = 1 
            visita.trabajador_id = 1  
            visita.save()
            return redirect('dashvisitas')  
    context = {'form': form}  
    return render(request, 'enfermero/Dashboard-RegistroV.html', context)

def pacientes(request):
    return render(request, 'enfermero/Dashboard-Pacientes.html')

def ultimasV(request):
    return render(request, 'enfermero/ultimasvisitas.html')

def enfpedidos(request):
    return render(request, 'enfermero/pedirOmnic.html')


#coordinador
def coordinador(request):
    return render(request, 'coordinador/dashboardCoordinador.html')

def coordpacientes(request):
    return render(request, 'coordinador/coordPacientes.html')


#tens
def tens(request):
    return render(request, 'tens/dashTens.html')

def dashvisitastens(request):
    return render(request, 'tens/dashvisitastens.html')

def controltens(request):
    return render(request, 'tens/ctrltens.html')

def ultvisitastens(request):
    return render(request, 'tens/ultvisitastens.html')

def invtens(request):
    return render(request, 'tens/invtens.html')

def pacientestens(request):
    return render(request, 'tens/pacientesTens.html')


#omnicell

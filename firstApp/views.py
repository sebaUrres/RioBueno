from django.shortcuts import render, redirect
from firstApp.models import *
from . import forms
from .forms import *
import logging

logger = logging.getLogger(__name__)

def session_required(function):
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session:
            request.session.flush()
            return redirect('/login/')
        return function(request, *args, **kwargs)
    return wrap

def login(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        
        try:
            trabajador = Trabajador.objects.get(rut=rut)
            
            if trabajador.contrasena == password:
                request.session['user_id'] = trabajador.id
                request.session['user_type'] = trabajador.tipo.nombre
                request.session['user_nombre'] = f"{trabajador.nombres} {trabajador.apellidos}"
                
                logger.info(f"Login exitoso - Usuario: {trabajador.nombres} {trabajador.apellidos}")
                
                if trabajador.tipo.nombre == 'enfermero':
                    return redirect('/enfermero/')
                elif trabajador.tipo.nombre == 'coordinador':
                    return redirect('/coordinador/')
                elif trabajador.tipo.nombre == 'tens':
                    return redirect('/tens/')
            else:
                return render(request, 'login.html', {'error_message': 'ContraseÃ±a incorrecta'})
                
        except Trabajador.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'RUT no encontrado'})
            
    return render(request, 'login.html')

def logout(request):
    if 'user_nombre' in request.session:
        logger.info(f"Logout - Usuario: {request.session.get('user_nombre')}")
    request.session.flush()
    request.session.set_expiry(1)
    return redirect('/login/')

@session_required
def enfermero(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    context = {
        'nombre_usuario': request.session.get('user_nombre', 'Usuario'),
        'tipo_usuario': request.session.get('user_type', 'Sin rol')
    }
    return render(request, 'enfermero/Dashboard-Enfermero.html', context)

@session_required
def inventario(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/inventario.html')

@session_required
def dashinsumos(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/dashboardinsumos.html')

@session_required
def dashvisitas(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/Dashboard-Visitas.html')

@session_required
def detvisita(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/detallesVpaciente.html')

@session_required
def regvisita(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    form = IngresoVisitaForms()
    if request.method == 'POST':
        form = IngresoVisitaForms(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.paciente_id = 1
            visita.trabajador_id = request.session.get('user_id')
            visita.save()
            return redirect('dashvisitas')
    context = {'form': form}
    return render(request, 'enfermero/Dashboard-RegistroV.html', context)

@session_required
def pacientes(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/Dashboard-Pacientes.html')

@session_required
def ultimasV(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/ultimasvisitas.html')

@session_required
def enfpedidos(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'enfermero/pedirOmnic.html')

@session_required
def coordinador(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    context = {
        'nombre_usuario': request.session.get('user_nombre', 'Usuario'),
        'tipo_usuario': request.session.get('user_type', 'Sin rol')
    }
    return render(request, 'coordinador/dashboardCoordinador.html', context)

@session_required
def coordpacientes(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'coordinador/coordPacientes.html')

@session_required
def tens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    context = {
        'nombre_usuario': request.session.get('user_nombre', 'Usuario'),
        'tipo_usuario': request.session.get('user_type', 'Sin rol')
    }
    return render(request, 'tens/dashTens.html', context)

@session_required
def dashvisitastens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'tens/dashvisitastens.html')

@session_required
def controltens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'tens/ctrltens.html')

@session_required
def ultvisitastens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'tens/ultvisitastens.html')

@session_required
def invtens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'tens/invtens.html')

@session_required
def pacientestens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'tens/pacientesTens.html')


#omnicell
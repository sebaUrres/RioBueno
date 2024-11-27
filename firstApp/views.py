from django.shortcuts import render, redirect
from firstApp.models import *
from . import forms
from .forms import *
import logging
from datetime import datetime

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
                elif trabajador.tipo.nombre == 'omnicell':
                    return redirect('/omnicell/')
            else:
                return render(request, 'login.html', {'error_message': 'RUT o Contraseña incorrecta'})
                
        except Trabajador.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'RUT o Contraseña incorrecta'})
            
    return render(request, 'login.html')

def logout(request):
    if 'user_nombre' in request.session:
        logger.info(f"Logout - Usuario: {request.session.get('user_nombre')}")
    request.session.flush()
    request.session.set_expiry(1)
    return redirect('/login/')


# ----------------------------ENFERMERO---------------------------------
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
    
    # Obtener el ID del trabajador logeado
    trabajador_id = request.session.get('user_id')
    
    # Filtrar los elementos del inventario por el ID del trabajador
    inventario_items = Inventario.objects.filter(trabajador_id=trabajador_id).select_related('item')
    
    context = {
        'inventario': inventario_items, 
        'nombre_usuario': request.session.get('user_nombre', 'Usuario'),
        'tipo_usuario': request.session.get('user_type', 'Sin rol')
    }
    return render(request, 'enfermero/inventario.html', context)

@session_required
def inventarioAgregar(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    form = IngresoInventarioForms()
    if request.method == 'POST':
        form = IngresoInventarioForms(request.POST)
        if form.is_valid():
            item_id = request.POST.get('insumo')
            trabajador_id = request.session.get('user_id')
            
            # Verificar si el item ya existe en el inventario
            try:
                item_existente = Inventario.objects.get(item_id=item_id, trabajador_id=trabajador_id)
                # Si existe, sumar la cantidad
                item_existente.cantidad += form.cleaned_data['cantidad']  # Asegúrate de que 'cantidad' esté en el formulario
                item_existente.save()
            except Inventario.DoesNotExist:
                # Si no existe, crear un nuevo registro
                item = form.save(commit=False)
                item.item_id = item_id
                item.trabajador_id = trabajador_id
                item.save()
                
            return redirect('/inventario')
    
    insumos = Insumos.objects.all() 
    context = {'form': form, 'insumos': insumos}
    return render(request, 'enfermero/inventarioAgregar.html', context)

@session_required
def inventarioSumar(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item = Inventario.objects.get(id=id)
    item.cantidad += 1  
    item.save()
    return redirect('/inventario')

@session_required
def inventarioRestar(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item = Inventario.objects.get(id=id)
    item.cantidad -= 1 
    if item.cantidad <= 0:
        item.delete() 
    else:
        item.save() 
    
    return redirect('/inventario')

@session_required
def inventarioBorrar(request,id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item=Inventario.objects.get(id=id)
    item.delete()
    return redirect("/inventario")

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
def detvisita(request, paciente_id):  
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    # Filtrar las visitas del paciente específico
    visitas = Visita.objects.filter(paciente_id=paciente_id).select_related('paciente').all()
    
    context = {'visitas': visitas}  # Agrega las visitas al contexto
    return render(request, 'enfermero/detallesVpaciente.html', context)

@session_required
def regvisita(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    form = IngresoVisitaForms()
    pacientes = Paciente.objects.all()
    if request.method == 'POST':
        form = IngresoVisitaForms(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.paciente_id = request.POST.get('paciente')
            visita.trabajador_id = request.session.get('user_id')
            visita.save()
            return redirect('/dashvisitas')
    context = {'form': form, 'pacientes': pacientes}
    return render(request, 'enfermero/Dashboard-RegistroV.html', context)

@session_required
def pacientes(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    #pacientes = Paciente.objects.all()
    pacientes = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')).all()
    context = {'pacientes': pacientes}
    return render(request, 'enfermero/Dashboard-Pacientes.html', context)

@session_required
def regPaciente(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    form = RegistroPacienteForms()
    if request.method == 'POST':
        form = RegistroPacienteForms(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()
            return redirect('/pacientes')
    context = {'form': form}
    return render(request, 'enfermero/registroPaciente.html', context)


@session_required
def ultimasV(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    trabajador_id = request.session.get('user_id')
    visitas = Visita.objects.filter(trabajador_id=trabajador_id).select_related('paciente').all().order_by('-fechavisita')  
    context = {'visitas': visitas}  # Agrega las visitas al contexto
    return render(request, 'enfermero/ultimasvisitas.html', context)

@session_required
def enfpedidos(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    form = IngresoPedidoOmniForms()
    if request.method == 'POST':
        form = IngresoPedidoOmniForms(request.POST)
        if form.is_valid():
            item_id = request.POST.get('insumo')
            trabajador_id = request.session.get('user_id')
            pedido = form.save(commit=False)
            pedido.item_id = item_id
            pedido.trabajador_id = trabajador_id
            pedido.estado = 1
            pedido.fecha = datetime.now()
            pedido.save()
            return redirect('/dashinsumos')
    
    inventario_omnicell_items = InventarioOmnicell.objects.all()
    context = {
        'items': inventario_omnicell_items,
        'form': form
    }
    return render(request, 'enfermero/pedirOmnic.html', context)

# -------------------------------COORDINADOR-----------------

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

# ---------------------TENS----------------------------------

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
    
    form = IngresoVisitaForms()
    pacientes = Paciente.objects.all()
    if request.method == 'POST':
        form = IngresoVisitaForms(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.paciente_id = request.POST.get('paciente')
            visita.trabajador_id = request.session.get('user_id')
            visita.save()
            return redirect('/dashvisitastens')
    context = {'form': form, 'pacientes': pacientes}
    return render(request, 'tens/ctrltens.html', context)

@session_required
def ultvisitastens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    trabajador_id = request.session.get('user_id')
    visitas = Visita.objects.filter(trabajador_id=trabajador_id).select_related('paciente').all().order_by('-fechavisita')  
    context = {'visitas': visitas}  

    return render(request, 'tens/ultvisitastens.html', context)

@session_required
def invtens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    trabajador_id = request.GET.get('enfermero') 
    # Filtrar los elementos del inventario por el ID del trabajador seleccionado
    inventario_items = Inventario.objects.filter(trabajador_id=trabajador_id)

    enfermeros = Trabajador.objects.filter(tipo__nombre='enfermero')
    
    context = {
        'inventario': inventario_items, 
        'pacientes': enfermeros
    }
    return render(request, 'tens/invTens.html', context)



@session_required
def pacientestens(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    pacientes = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')).all()
    context = {'pacientes': pacientes}
    return render(request, 'tens/pacientesTens.html',context)

@session_required
def detvisitatens(request, paciente_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    visitas = Visita.objects.filter(paciente_id=paciente_id).select_related('paciente').all()
    context = {'visitas': visitas}
    return render(request, 'tens/pacientedetalle.html',context)




# -------------------------------OMNICELL-------------------------

@session_required
def omni(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    context = {
        'nombre_usuario': request.session.get('user_nombre', 'Usuario'),
        'tipo_usuario': request.session.get('user_type', 'Sin rol')
    }
    return render(request, 'omnicell/dashOmni.html', context) 

@session_required
def bodegaOmni(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    # Cambiar para obtener todos los elementos de la tabla InventarioOmnicell
    inventario_items = InventarioOmnicell.objects.all()  # Cambiado de Inventario a InventarioOmnicell
    
    context = {
        'inventario': inventario_items
    }
    return render(request, 'omnicell/bodegaOmni.html', context)

@session_required
def bodegaAgregar(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    form = IngresoBodegaOmniForms()
    if request.method == 'POST':
        form = IngresoBodegaOmniForms(request.POST)
        if form.is_valid():
            item_id = request.POST.get('insumo')
            
            try:
                item_existente = InventarioOmnicell.objects.get(item_id=item_id)
                # Si existe, sumar la cantidad
                item_existente.cantidad += form.cleaned_data['cantidad']  # Asegúrate de que 'cantidad' esté en el formulario
                item_existente.save()
            except InventarioOmnicell.DoesNotExist:
                # Si no existe, crear un nuevo registro
                item = form.save(commit=False)
                item.item_id = item_id
                item.save()
                
            return redirect('/bodegaOmni')
    
    insumos = Insumos.objects.all() 
    context = {'form': form, 'insumos': insumos}
    return render(request, 'omnicell/bodegaAgregar.html', context)

@session_required
def bodegaSumar(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item = InventarioOmnicell.objects.get(id=id)
    item.cantidad += 1  
    item.save()
    return redirect('/bodegaOmni')

@session_required
def bodegaRestar(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item = InventarioOmnicell.objects.get(id=id)
    item.cantidad -= 1 
    if item.cantidad <= 0:
        item.delete() 
    else:
        item.save() 
    
    return redirect('/bodegaOmni')

@session_required
def bodegaBorrar(request,id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    item=InventarioOmnicell.objects.get(id=id)
    item.delete()
    return redirect("/bodegaOmni")

@session_required
def pedidosOmni(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    pedidos = PedidoOmnicell.objects.select_related('trabajador').filter(estado=1) 
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'omnicell/pedidosOmni.html', context)

@session_required
def marcar_listo(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    pedido = PedidoOmnicell.objects.get(id=id)
    pedido.estado = 0  
    pedido.save()
    
    return redirect('/pedidosOmni')

@session_required
def historialPedidos(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    pedidos = PedidoOmnicell.objects.select_related('trabajador').all()
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'omnicell/historialPedidos.html', context)
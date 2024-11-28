from django.shortcuts import render, redirect
from firstApp.models import *
from . import forms
from .forms import *
import logging
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

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
            
            if trabajador.estado == 0:
                return render(request, 'login.html', {'error_message': 'El usuario está inactivo. Por favor pidale al coordinador correspondiente que reactive su cuenta'})
            
            if check_password(password,trabajador.contrasena):
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
                item_existente.cantidad += form.cleaned_data['cantidad']  
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
def detvisitaedit(request, visita_id):  
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    visita = Visita.objects.get(id=visita_id)
    form = IngresoVisitaForms(instance=visita)
    if request.method == "POST":
        form = IngresoVisitaForms(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect(f"/detvisita/{visita.paciente_id}")
    
    data = {'form': form, 'visita': visita}  
    return render(request, 'enfermero/detallesVpacienteedit.html', data)

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

def pacientessearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    query = request.GET.get('query', '')
    
    
    if query != "":
        resultados = Paciente.objects.filter(nombres__icontains=query).annotate(cantidad_visitas=models.Count('visita'))
    else:
        resultados = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')) 
    
    data = {'pacientes': resultados}
    return render(request, 'enfermero/Dashboard-Pacientessearch.html', data)

@session_required
def regPaciente(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    form = RegistroPacienteForms()
    if request.method == 'POST':
        form = RegistroPacienteForms(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            
            # Obtener el estado de los checkboxes
            condiciones = []
            if request.POST.get('asma'):
                condiciones.append("asma ")
            if request.POST.get('diabetes'):
                condiciones.append("diabetes ")
            if request.POST.get('artritis'):
                condiciones.append("artritis ")
            if request.POST.get('polvo'):
                condiciones.append("polvo ")
            if request.POST.get('moho'):
                condiciones.append("moho ")
            if request.POST.get('polen'):
                condiciones.append("polen ")
            
            
            # Unir las condiciones en un solo string
            paciente.condiciones = " ".join(condiciones)  
            
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
def ultimasVsearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    filtros = Q(trabajador_id=request.session.get('user_id')) 

    if fecha_desde:
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            filtros &= Q(fechavisita__gte=fecha_desde)
        except ValueError:
            pass  

    if fecha_hasta:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            filtros &= Q(fechavisita__lte=fecha_hasta)
        except ValueError:
            pass  

    resultados = Visita.objects.filter(filtros)
    data = {'visitas': resultados}
    return render(request, 'enfermero/ultvisitassearch.html', data)

@session_required
def ultvisitasedit(request, visita_id):  
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    visita = Visita.objects.get(id=visita_id)
    form = IngresoVisitaForms(instance=visita)
    if request.method == "POST":
        form = IngresoVisitaForms(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect("/ultvisitas")
    
    data = {'form': form, 'visita': visita}  
    return render(request, 'enfermero/ultimasvisitasedit.html', data)

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
    
    inventario_omnicell_items = Insumos.objects.all()
    context = {
        'items': inventario_omnicell_items,
        'form': form
    }
    return render(request, 'enfermero/pedirOmnic.html', context)


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
def ultvisitastenssearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    filtros = Q(trabajador_id=request.session.get('user_id')) 

    if fecha_desde:
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            filtros &= Q(fechavisita__gte=fecha_desde)
        except ValueError:
            pass  

    if fecha_hasta:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            filtros &= Q(fechavisita__lte=fecha_hasta)
        except ValueError:
            pass  

    resultados = Visita.objects.filter(filtros)
    data = {'visitas': resultados}
    return render(request, 'tens/ultvisitassearchtens.html', data)

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

def pacientestenssearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    query = request.GET.get('query', '')
    
    
    if query != "":
        resultados = Paciente.objects.filter(nombres__icontains=query).annotate(cantidad_visitas=models.Count('visita'))
    else:
        resultados = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')) 
    
    data = {'pacientes': resultados}
    return render(request, 'tens/pacientestenssearch.html', data)

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
                item_existente.cantidad += form.cleaned_data['cantidad']  
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
    
    pedidos = PedidoOmnicell.objects.select_related('trabajador').filter(estado=0)
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'omnicell/historialPedidos.html', context)

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
    pacientes = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')).all()
    context = {'pacientes': pacientes}
    return render(request, 'coordinador/coordPacientes.html', context)

@session_required
def coordpacientessearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    query = request.GET.get('query', '')
    
    
    if query != "":
        resultados = Paciente.objects.filter(nombres__icontains=query).annotate(cantidad_visitas=models.Count('visita'))
    else:
        resultados = Paciente.objects.annotate(cantidad_visitas=models.Count('visita')) 
    
    data = {'pacientes': resultados}
    return render(request, 'coordinador/coordPacientes.html',data)

@session_required
def coorddetvisita(request, paciente_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    visitas = Visita.objects.filter(paciente_id=paciente_id).select_related('paciente').all()
    
    context = {'visitas': visitas}
    return render(request, 'coordinador/coorddetallevisita.html', context)


@session_required
def coordultimasvisitas(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    visitas = Visita.objects.select_related('paciente', 'trabajador').all().order_by('-fechavisita')  
    context = {'visitas': visitas}  

    return render(request, 'coordinador/ultimasvisitas.html', context)

@session_required
def coordultimasvisitassearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    filtros = Q() 

    if fecha_desde:
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            filtros &= Q(fechavisita__gte=fecha_desde)
        except ValueError:
            pass  

    if fecha_hasta:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            filtros &= Q(fechavisita__lte=fecha_hasta)
        except ValueError:
            pass  

    resultados = Visita.objects.filter(filtros)
    data = {'visitas': resultados}
    return render(request, 'coordinador/ultimasvisitassearch.html', data)

@session_required
def registrousuario(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    form = RegistroUsuarioForms()
    tipos_usuario = TipoUsuario.objects.all()
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.estado = 1

            paciente.contrasena = make_password(form.cleaned_data['contrasena'])

            paciente.save()
            return redirect('/usuarios')
        else:
            print(form.errors)
    context = {'form': form, 'tipos_usuario': tipos_usuario}
    return render(request, 'coordinador/registrousuario.html', context)

@session_required
def usuarios(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    pacientes = Trabajador.objects.all()
    context = {'usuarios': pacientes}
    return render(request, 'coordinador/coordusuarios.html', context)

@session_required
def desactivar(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    trabajador = Trabajador.objects.get(id=id)
    trabajador.estado = 0 if trabajador.estado == 1 else 1 
    trabajador.save()
    
    return redirect('/usuarios')  


def coordusuariossearch(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    query = request.GET.get('query', '')
    
    if query:
        resultados = Trabajador.objects.filter(nombres__icontains=query)
    else:
        resultados = Trabajador.objects.all() 
    
    data = {'usuarios': resultados}
    return render(request, 'coordinador/coordusuariossearch.html', data)

@session_required
def editusuario(request, id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    usuario = Trabajador.objects.get(id=id)
    tipos_usuario = TipoUsuario.objects.all()
    
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST, instance=usuario)  
        if form.is_valid():
            form.save()  
            return redirect('/usuarios')
    else:
        form = RegistroUsuarioForms(instance=usuario) 
    
    context = {'form': form, 'tipos_usuario': tipos_usuario, 'usuario': usuario}
    return render(request, 'coordinador/editusuario.html', context)


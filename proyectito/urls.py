"""
URL configuration for proyectito project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstApp import views as app



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', app.login, name='login'),
    path('logout/', app.logout, name='logout'),
    #enfermero
    path("enfermero/", app.enfermero),
    path("inventario/", app.inventario),
    path("inventarioAgregar/",app.inventarioAgregar),
    path("inventarioSumar/<int:id>/", app.inventarioSumar),
    path("inventarioRestar/<int:id>/", app.inventarioRestar),
    path("inventarioBorrar/<int:id>/", app.inventarioBorrar),
    path("dashinsumos/", app.dashinsumos),
    path("dashvisitas/", app.dashvisitas),
    path("detvisita/<int:paciente_id>/", app.detvisita, name='detvisita'),
    path("detvisitaedit/<int:visita_id>/", app.detvisitaedit),
    path("regvisita/", app.regvisita),
    path("pacientes/", app.pacientes),
    path("pacientessearch/", app.pacientessearch),
    path("regPaciente/", app.regPaciente),
    path("ultvisitas/", app.ultimasV),
    path("ultvisitassearch/", app.ultimasVsearch),
    path("ultvisitasedit/<int:visita_id>/", app.ultvisitasedit),
    path("pedidoomnicell/", app.enfpedidos),


    #tens
    path("tens/", app.tens),
    path("dashvisitastens/", app.dashvisitastens),
    path("controltens/", app.controltens),
    path("ultvisitastens/", app.ultvisitastens),
    path("ultvisitassearchtens/", app.ultvisitastenssearch),
    path("invtens/", app.invtens),
    path("pacientestens/", app.pacientestens),
    path("pacientestenssearch/", app.pacientestenssearch),
    path("detvisitatens/<int:paciente_id>/", app.detvisitatens),


    #omnicell
    path("omnicell/", app.omni),
    path("bodegaOmni/", app.bodegaOmni),
    path("bodegaAgregar/",app.bodegaAgregar),
    path("bodegaSumar/<int:id>/", app.bodegaSumar),
    path("bodegaRestar/<int:id>/", app.bodegaRestar),
    path("bodegaBorrar/<int:id>/", app.bodegaBorrar),
    path("pedidosOmni/",app.pedidosOmni),
    path("marcarListo/<int:id>/", app.marcar_listo),
    path("historialPedidos/",app.historialPedidos),

    #coordinador
    path("coordinador/", app.coordinador),
    path("coordPacientes/", app.coordpacientes),
    path("coordPacientessearch/", app.coordpacientessearch),    
    path("coorddetvisita/<int:paciente_id>/", app.coorddetvisita),   
    path("coordultvisitas/", app.coordultimasvisitas),
    path("coordultvisitassearch/", app.coordultimasvisitassearch),
    path("usuarios/", app.usuarios),
    path("registrousuario/", app.registrousuario),
    path("desactivar/<int:id>/", app.desactivar, name='desactivar'),
    path("coordusuariossearch/", app.coordusuariossearch),
    path("editusuario/<int:id>/", app.editusuario),
]

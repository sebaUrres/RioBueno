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
    path("login/", app.login),
    path("enfermero/", app.enfermero),
    path("coordinador/", app.coordinador),
    path("inventario/", app.inventario),
    path("dashinsumos/", app.dashinsumos),
    path("dashvisitas/", app.dashvisitas),
    path("detvisita/", app.detvisita),
    path("regvisita/", app.regvisita),
    path("pacientes/", app.pacientes),
    path("ultvisitas/", app.ultimasV),
    path("pedidoomnicell/", app.enfpedidos)
]

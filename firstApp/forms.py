from django import forms
from firstApp.models import *

class TrabajadorForms(forms.ModelForm):
    class Meta:
        model= Trabajador
        fields='__all__'

class IngresoVisitaForms(forms.ModelForm):
    class Meta:
        model= Visita
        fields=['antecedentes','fechavisita','presionart', 'frecuenciacard', 'saturometria', 'temperatura', 'hemoglucotest', 'motivovisita', 'indicaciones', 'observaciones']


class RegistroPacienteForms(forms.ModelForm):
    class Meta:
        model= Paciente
        fields=['nombres','apellidos','rut','edad','direccion']

class IngresoInventarioForms(forms.ModelForm):
    class Meta:
        model= Inventario
        fields=['cantidad']

class IngresoPedidoOmniForms(forms.ModelForm):
    class Meta:
        model= PedidoOmnicell
        fields=['cantidad']

class IngresoBodegaOmniForms(forms.ModelForm):
    class Meta:
        model=InventarioOmnicell
        fields=['cantidad']
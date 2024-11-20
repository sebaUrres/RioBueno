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



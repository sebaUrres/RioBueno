from django.db import models

class Trabajador(models.Model):
    rol=models.CharField(max_length=15)#el rol sera visto para nosotros como un numero
    rut=models.CharField(max_length=50)
    contraseña=models.CharField(max_length=20)
    nombre=models.CharField(max_length=15)
    segNom=models.CharField(max_length=15)
    apePaterno=models.CharField(max_length=15)
    apeMaterno=models.CharField(max_length=15)
    email=models.EmailField()



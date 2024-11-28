from django.db import models

class TipoUsuario(models.Model):
    nombre = models.TextField()


class Trabajador(models.Model):
    nombres = models.TextField(max_length=30)
    apellidos = models.TextField(max_length=30)
    telefono = models.TextField(max_length=12)
    email = models.EmailField()
    rut = models.TextField(unique=True, max_length=12)
    contrasena = models.TextField(max_length=20)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    estado = models.BooleanField(default=1)


class Paciente(models.Model):
    nombres = models.TextField(max_length=30)
    apellidos = models.TextField(max_length=30)
    rut = models.TextField(unique=True, max_length=12)
    edad = models.IntegerField()
    direccion = models.TextField(blank=True, null=True, max_length=30)
    condiciones = models.TextField(max_length=100)


class Visita(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    antecedentes = models.TextField(blank=True, null=True)
    fechavisita = models.DateTimeField()
    presionart = models.TextField(blank=True, null=True,max_length=10)
    frecuenciacard = models.TextField(blank=True, null=True,max_length=10)
    saturometria = models.TextField(blank=True, null=True,max_length=10)
    temperatura = models.TextField(blank=True, null=True,max_length=10)
    hemoglucotest = models.TextField(blank=True, null=True,max_length=10)
    motivovisita = models.TextField()
    indicaciones = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

class Insumos(models.Model):
    item = models.TextField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)
    metodouso = models.TextField(blank=True, null=True,max_length=100)
    contraindicaciones = models.TextField(blank=True, null=True,max_length=100)

    def __str__(self):
        return self.item

class PedidoOmnicell(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    item = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado=models.BooleanField(default=1)
    fecha=models.DateTimeField()

class Inventario(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    item = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class InventarioOmnicell(models.Model):
    item = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()




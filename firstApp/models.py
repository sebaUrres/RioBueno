from django.db import models

class TipoUsuario(models.Model):
    nombre = models.TextField()


class Trabajador(models.Model):
    nombres = models.TextField()
    apellidos = models.TextField()
    telefono = models.TextField()
    email = models.EmailField()
    rut = models.TextField(unique=True)
    contraseña = models.TextField()
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    estado = models.IntegerField(default=1)


class Paciente(models.Model):
    nombres = models.TextField()
    apellidos = models.TextField()
    rut = models.TextField(unique=True)
    edad = models.IntegerField()
    direccion = models.TextField(blank=True, null=True)


class Visita(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    antecedentes = models.TextField(blank=True, null=True)
    fechavisita = models.DateTimeField()
    presionart = models.TextField(blank=True, null=True)
    frecuenciacard = models.TextField(blank=True, null=True)
    saturometria = models.TextField(blank=True, null=True)
    temperatura = models.TextField(blank=True, null=True)
    hemoglucotest = models.TextField(blank=True, null=True)
    motivovisita = models.TextField()
    indicaciones = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)


class Inventario(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    item = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    metodouso = models.TextField(blank=True, null=True)
    contraindicaciones = models.TextField(blank=True, null=True)


class PedidoOmnicell(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    item = models.TextField()
    cantidad = models.IntegerField()

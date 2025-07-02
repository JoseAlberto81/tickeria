from django.db import models

class Ticket(models.Model):
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En progreso', 'En progreso'),
        ('Cerrado', 'Cerrado'),
    ]
    PRIORIDAD_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Importante', 'Importante'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')
    titulo = models.CharField(max_length=200, blank=False)
    solicitante = models.CharField(max_length=100, blank=False)
    email = models.EmailField()
    asignado = models.CharField(max_length=100, blank=True, default='HelpDesk')
    fecha_esperada = models.DateField(null=True, blank=True)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, blank=True)
    etiqueta = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    respuesta = models.TextField(blank=True, null=True)
    firma = models.ImageField(upload_to='firmas/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.solicitante}"
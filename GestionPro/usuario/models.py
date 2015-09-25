from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    ('1', 'Rol de Sistema'),
    ('2', 'Rol de Proyecto'),
    )

class Usuario(User):

    celular = models.PositiveIntegerField(default=0, blank=True, verbose_name='Telefono/Celular:')
    cedula = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=50, null=False, blank=True)

def __unicode__(self):
    return self.username

def get_absolute_url(self):
        return reverse('editar_usuario', kwargs={'pk': self.pk})

class Permiso(models.Model):
    """Clase que representa a los Permisos"""
    nombre = models.CharField(unique=True, max_length=50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)

    def __unicode__(self):
        return self.nombre

class Rol(models.Model):
    """
    Clase que representa a los roles
    """
    nombre = models.CharField(unique=True, max_length=50)
    categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)
    descripcion = models.TextField(null=True, blank=True)
    fecHor_creacion = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)
    usuario_creador = models.ForeignKey(User, null=True)
    permisos = models.ManyToManyField(Permiso, through='RolPermiso')

    def __unicode__(self):
        return self.nombre
class RolPermiso(models.Model):
    """Clase que relaciona Rol con Permiso"""
    rol = models.ForeignKey(Rol)
    permiso = models.ForeignKey(Permiso)

class UsuarioRolSistema (models.Model):
    """Clase que relaciona Usuario, Rol y Sistema"""
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol)

    class Meta:
        unique_together = [("usuario", "rol")]
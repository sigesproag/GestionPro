from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Usuario(User):

    celular = models.PositiveIntegerField(default=0, blank=True, verbose_name='Telefono/Celular:')
    cedula = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=50, null=False, blank=True)

def __unicode__(self):
    return self.username

def get_absolute_url(self):
        return reverse('editar_usuario', kwargs={'pk': self.pk})
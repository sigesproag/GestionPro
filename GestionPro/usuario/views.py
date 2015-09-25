from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from models import Usuario,UsuarioRolSistema
from django.contrib.auth.models import User
from forms import FormUsuario, FormUsuarioChange, AdminPasswordChangeForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def inicio(request):
    return render_to_response('base.html', context_instance=RequestContext(request))

@login_required(login_url='/usuario/login')
def nuevo_user(request):

    """
    :param request: contiene los datos de la pagina que lo llamo
    :return: crearUsuario.html, pagina en la cual se crea el usuario
    Metodo para crear un nuevo usuario
    """
    user = User.objects.get(username=request.user.username)
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    form = FormUsuario()
    if request.method == 'POST':
        print 'hola'
        form = FormUsuario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            u = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,password=password_one)
            u.save()
            return HttpResponseRedirect("/usuario/lista/")
    else:
        ctx = {'form':form,
               'user':user,
               'crear_usuario': 'crear usuario' in permisos}
        return 	render_to_response('usuarios/nuevo_usuario.html',ctx,context_instance=RequestContext(request))
    ctx = {'form':form,
           'user':user,
           'crear_usuario': 'crear usuario' in permisos}
    return render_to_response('usuarios/nuevo_usuario.html',ctx,context_instance=RequestContext(request))

# @login_required(login_url='/usuario/login')
# @permission_required('auth.add_user', login_url='/usuario/login')
# def nuevo_user(request):
#     if request.method == 'POST':
#         formulario = FormUsuario(request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             return HttpResponseRedirect('/usuario/lista/')
#     else:
#         formulario = FormUsuario()
#         return render_to_response('usuarios/nuevo_usuario.html', {'formulario': formulario},
#                                   context_instance=RequestContext(request))


def iniciar_sesion(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            username = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=username, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/index/')
                else:
                    return HttpResponseRedirect('/index/')
            else:
                return HttpResponseRedirect('/index/')
    else:
        formulario = AuthenticationForm()

    return render_to_response('usuarios/login.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


@login_required(login_url='/usuario/login')
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/index/')


class UsuarioList(ListView):
    model = Usuario
    template_name = 'usuarios/lista_usuario.html'


class UsuarioDelete(DeleteView):
    model = Usuario
    template_name = 'usuarios/borrar_usuario.html'
    success_url = '/usuario/lista/'


class UpdateUser(UpdateView):
    template_name = 'usuarios/modificar_usuario.html'
    model = Usuario
    form_class = FormUsuarioChange
    success_url = '/usuario/lista/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateUser, self).dispatch(*args, **kwargs)


@login_required(login_url='/usuario/login')
def cambio_clave(request):
    if request.method == 'POST':
        formulario = AdminPasswordChangeForm(request.POST, request.user)
        if formulario.is_valid:
            formulario.save()
            return redirect('/index/')
    else:
        formulario = AdminPasswordChangeForm(request.POST)
        return render_to_response('usuarios/cambiar_clave.html', {'formulario': formulario},
                                  context_instance=RequestContext(request))

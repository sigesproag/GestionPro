
# Create your views here.
__author__ = 'rvidal'
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/usuario/login')
def index(request):
    """
    Vista para el login
    :param request: Recibe un request HTTP
    :return: la pagina principal si la autenticacion tuvo exito
    """
    return render(request, 'base.html',{'user': request.user})


def logout_view(request):
    """
    Vista para el logout
    :param request: Recibe un request HTTP
    :return: retorna a la pantalla de login
    """
    logout(request)
    return redirect('/login/?next=/')

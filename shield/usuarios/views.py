import requests
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroForm
from firebase_admin import auth
from django.conf import settings
from .models import Usuario
from django.views.decorators.cache import never_cache
import os
#encontré un bug, al momento de iniciar sesión me manda
# al index, y al retrocede la pagina varias veces me manda
# al login y al escribir cualquier cosa en las credenciales
# me sale como si fuera un usuario que existe pero no existe 
# y entra normal al index -------- SOLUCIONADO ------------- @never_cache ------------

#@never_cache, hace que no guarde el cache del login y registrar, al final ese error solo era visual pero igual lo puse para que no sea vea así
#
FIREBASE_WEB_API_KEY = "AIzaSyDoGQNvfqGc-9d5hXTYgT8RNzLX-v0eBP0"

#Proteger vistas para que no las salten sin logearse
#-----------------------------------------------------------
def login_required_firebase(view_func):
    def wrapper(request, *args, **kwargs):
        if 'id_token' not in request.session:
            return redirect('login')  # Si no tiene token, redirigir al login
        return view_func(request, *args, **kwargs)
    return wrapper
#-----------------------------------------------------------

@never_cache
def registrar(request):
    error_message = None

    # Si el usuario ya está autenticado, redirigir al index
    if 'id_token' in request.session:
        return redirect('casilleros:casilleros_list')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usuario = form.cleaned_data['usuario']

            try:
                # Crear usuario en Firebase
                user = auth.create_user(
                    email=email,
                    password=password,
                    display_name=usuario
                )
                
                # Guardar en la base de datos local
                Usuario.objects.create(email=email, nickname=usuario)

                return redirect('casilleros:casilleros_list')

            except Exception as e:
                error_message = str(e)

        else:
            error_message = "Formulario inválido. Verifica los campos."
    
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form, 'error_message': error_message})

@never_cache
def login(request):
    error_message = None

    # Si el usuario ya tiene un token, redirigir al index
    if 'id_token' in request.session:
        return redirect('casilleros:casilleros_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']  # Puede ser correo o nickname
            password = form.cleaned_data['password']

            # Verificar si el usuario es un correo o un nickname
            if '@' in usuario:
                email = usuario  # Es un correo
            else:
                # Buscar el correo asociado al nickname en la base de datos local
                try:
                    user = Usuario.objects.get(nickname=usuario)
                    email = user.email
                except Usuario.DoesNotExist:
                    error_message = "El nombre de usuario no existe"
                    return render(request, 'usuarios/login.html', {'form': form, 'error_message': error_message})

            # Autenticar con Firebase usando el correo y la contraseña
            try:
                data = {
                    'email': email,
                    'password': password,
                    'returnSecureToken': True
                }
                # Petición a Firebase para la autenticación
                result = requests.post(
                    f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}", 
                    json=data
                )
                result_data = result.json()

                # Si la autenticación es exitosa
                if 'idToken' in result_data:
                    request.session['id_token'] = result_data['idToken']
                    request.session['email'] = email  # Guardar el email en la sesión
                    return redirect('casilleros:casilleros_list')  # Redirigir al index
                else:
                    error_message = "Credenciales inválidas. Por favor, verifica tu correo y contraseña."

            except requests.exceptions.RequestException as e:
                error_message = f"Error de conexión: {str(e)}"
            except Exception as e:
                error_message = f"Error inesperado: {str(e)}"
    
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form, 'error_message': error_message})

@login_required_firebase
def index(request):
    return render(request, 'usuarios/index.html')

@login_required_firebase
def casilleros(request):
    return render(request, 'usuarios/casilleros.html')

@login_required_firebase
def detalle(request, nombre, ubicacion, precio, descripcion):
    contexto = {
        'nombre': nombre,
        'ubicacion': ubicacion,
        'precio': precio,
        'descripcion': descripcion
    }
    return render(request, 'usuarios/casilleros/detalle.html', contexto)

@login_required_firebase
def logout(request):
    try:
        del request.session['id_token']  # Eliminar el token de Firebase de la sesión
    except KeyError:
        pass
    return redirect('login')  # Redirigir al login después de cerrar sesión




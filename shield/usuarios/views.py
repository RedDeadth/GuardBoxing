import requests
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroForm
from firebase_admin import auth
from django.conf import settings
from .models import Usuario
from django.views.decorators.cache import never_cache
import os
from django.http import JsonResponse


FIREBASE_WEB_API_KEY = "AIzaSyC3ERiX-ARDhZq4m0NulXAjRExyHQqral4"


def login_required_firebase(view_func):
    def wrapper(request, *args, **kwargs):
        if 'id_token' not in request.session:
            return redirect('login') 
        return view_func(request, *args, **kwargs)
    return wrapper

@never_cache

def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Procesar el registro
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

                return JsonResponse({'success': True, 'message': 'Usuario registrado exitosamente.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Formulario inválido.'}, status=400)

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        # Verificar si el usuario es un correo o un nickname
        email = None
        if '@' in usuario:
            email = usuario
        else:
            try:
                user = Usuario.objects.get(nickname=usuario)
                email = user.email
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'El nombre de usuario no existe'})

        # Autenticar con Firebase
        try:
            data = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
            result = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}",
                json=data
            )
            result_data = result.json()

            if 'idToken' in result_data:
                return JsonResponse({'success': True, 'id_token': result_data['idToken'], 'email': email})
            else:
                return JsonResponse({'success': False, 'error': 'Credenciales inválidas.'})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

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

#ANDROID
def verificar_token(request):
    token = request.POST.get('id_token')  # Obtén el token del POST

    try:
        # Verifica el token usando Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        return JsonResponse({'valid': True, 'uid': decoded_token['uid']})
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)}, status=401)


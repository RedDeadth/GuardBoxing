from django.shortcuts import render, redirect
from firebase_admin import db
from django.contrib.auth.decorators import login_required
from .utils import login_required_firebase  # Importar el decorador personalizado
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CasilleroSerializer
from django.http import JsonResponse
from .models import Casillero

@api_view(['GET'])
def lista_casilleros(request):
    """
    Obtiene los casilleros de Firebase y los envía como respuesta JSON.
    """
    ref = db.reference('casilleros')  # Obtiene la referencia de 'casilleros' en Firebase
    casilleros = ref.get()  # Obtiene los datos de los casilleros

    return JsonResponse(casilleros)

def casilleros_list(request):
    ref = db.reference('casilleros')
    casilleros = ref.get()  # Obtiene todos los casilleros desde Firebase Realtime Database
    return render(request, 'casilleros/list.html', {'casilleros': casilleros})


# Crear nuevo casillero

# Creación de un nuevo casillero
def crear_casillero(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')

        # Referencia a la ubicación en Firebase para guardar el casillero
        ref = db.reference('casilleros')
        ref.child(id).set({
            'nombre': nombre,
            'ubicacion': ubicacion,
            'precio': precio,
            'descripcion': descripcion,
            'estado_bloqueo': False,  # El estado de bloqueo ahora es un booleano
            'apertura': 'cerrado',  # El estado de apertura puede ser 'abierto' o 'cerrado'
        })

        return redirect('casilleros:casilleros_list')
    
    return render(request, 'casilleros/crear.html')

def detalle_casillero(request, id):
    # Referencia a los casilleros en Firebase
    ref = db.reference('casilleros')
    casilleros = ref.get()

    # Obtener el casillero usando el id como clave
    casillero = casilleros.get(id)  # Aquí estamos obteniendo el casillero por su id

    # Verificar si el casillero fue encontrado
    if casillero:
        return render(request, 'casilleros/detalle.html', {'casillero': casillero, 'id': id})
    else:
        # Si el casillero no existe, redirigir o mostrar un mensaje
        return render(request, 'casilleros/detalle.html', {'casillero': None, 'mensaje': 'Casillero no encontrado'})


def bloquear_casillero(request, id):
    ref = db.reference(f'casilleros/{id}')
    casillero = ref.get()

    # Cambiar el estado de bloqueo
    nuevo_estado = not casillero.get('estado_bloqueo', False)  # Alterna el estado
    ref.update({
        'estado_bloqueo': nuevo_estado
    })
    return JsonResponse({
        'estado_bloqueo': nuevo_estado,
        'mensaje': 'Bloqueado' if nuevo_estado else 'Desbloqueado'
    })

# Vista para abrir/cerrar casillero
def gestionar_apertura(request, id):
    ref = db.reference(f'casilleros/{id}')
    casillero = ref.get()

    # Cambiar el estado de apertura
    nuevo_estado_apertura = 'cerrado' if casillero.get('apertura') == 'abierto' else 'abierto'
    ref.update({
        'apertura': nuevo_estado_apertura
    })

    return JsonResponse({
        'apertura': nuevo_estado_apertura,
        'mensaje': 'Cerrado' if nuevo_estado_apertura == 'cerrado' else 'Abierto'
    })
from django.shortcuts import render, redirect
from firebase_admin import db
from django.contrib.auth.decorators import login_required
from .utils import login_required_firebase  # Importar el decorador personalizado
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CasilleroSerializer
from django.http import JsonResponse
from .models import Casillero
from datetime import datetime, timedelta

@api_view(['GET'])
def lista_casilleros(request):
    """
    Obtiene los casilleros de Firebase y los envía como respuesta JSON.
    """
    ref = db.reference('lockers')  # Obtiene la referencia de 'casilleros' en Firebase
    casilleros = ref.get()  # Obtiene los datos de los casilleros

    return JsonResponse(casilleros)

def casilleros_list(request):
    ref = db.reference('lockers')
    casilleros = ref.get()  # Obtiene todos los casilleros desde Firebase Realtime Database
    return render(request, 'casilleros/list.html', {'casilleros': casilleros})


# Crear nuevo casillero

# Creación de un nuevo casillero
def crear_casillero(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        location = request.POST.get('ubicacion')  # Campo 'ubicacion' en el formulario
        price = request.POST.get('precio')
        description = request.POST.get('descripcion')  # Campo 'descripcion' en el formulario

        userId = request.user.id
        # Referencia a la ubicación en Firebase para guardar el casillero
        ref = db.reference('lockers')

        existing_casillero = ref.child(id).get()  # Obtener el casillero existente

        # Verificar si el casillero ya existe
        if existing_casillero is not None:
            # Retornar un mensaje de error si el casillero ya existe
            return render(request, 'casilleros/crear.html', {
                'error': 'El casillero con este ID ya existe. Por favor, utiliza un ID diferente.'
            })
        
        ref.child(id).set({
            'location': location,  # Cambiado de 'ubicacion' a 'location'
            'price': price,
            'description': description,  # Cambiado de 'descripcion' a 'description'
            'blocked': False,  # Booleano para indicar si el casillero está bloqueado
            'open': False,  # Booleano para indicar si el casillero está abierto
            'occupied': False,  # Booleano para indicar si el casillero está ocupado
            'sharedwith': [],  # Lista vacía para compartir con usuarios
            'reservationendtime': None,  # Tiempo de finalización de la reserva
            'userId': userId,
        })

        return redirect('casilleros:casilleros_list')
    
    return render(request, 'casilleros/crear.html')


def detalle_casillero(request, id):
    # Referencia a los casilleros en Firebase
    ref = db.reference('lockers')
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
    if request.method == 'GET':
        # Referencia al casillero en Firebase
        ref = db.reference(f'lockers/{id}')
        casillero = ref.get()

        # Obtener el estado actual de 'blocked'
        blocked = casillero.get('blocked', False)

        # Invertir el estado de 'blocked'
        new_blocked_state = not blocked

        # Actualizar el estado en Firebase
        ref.update({
            'blocked': new_blocked_state
        })

        return JsonResponse({'blocked': new_blocked_state})

# Vista para abrir/cerrar casillero
def gestionar_apertura(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    # Cambiar el estado de apertura basado en el booleano "open"
    nuevo_estado_apertura = not casillero.get('open')  # Invierte el estado actual de "open"
    ref.update({
        'open': nuevo_estado_apertura
    })

    return JsonResponse({
        'open': nuevo_estado_apertura,
        'mensaje': 'Cerrado' if not nuevo_estado_apertura else 'Abierto'
    })


def abrir_casillero(request, id):
    if request.method == 'GET':
        # Referencia al casillero en Firebase
        ref = db.reference(f'lockers/{id}')
        casillero = ref.get()

        # Obtener el estado actual de 'open'
        open_state = casillero.get('open', False)

        # Invertir el estado de 'open'
        new_open_state = not open_state

        # Actualizar el estado en Firebase
        ref.update({
            'open': new_open_state
        })

        return JsonResponse({'open': new_open_state})


#RESERVAR UN CASILLERO, FUNCION API DE CLIENTE

@api_view(['POST'])
def reservar_casillero(request):
    casillero_id = request.data.get('id')
    user_id = request.data.get('userId')
    tiempo_reserva = request.data.get('reservationendtime')

    if not casillero_id or not user_id or not tiempo_reserva:
        return Response({'error': 'Faltan parámetros'}, status=400)
    
    # Referencia al casillero en Firebase
    ref = db.reference(f'lockers/{casillero_id}')
    casillero = ref.get()
    
    if casillero['occupied']:
        return Response({'error': 'El casillero ya está ocupado'}, status=400)
    
    # Actualizar los datos del casillero
    ref.update({
        'userId': user_id,
        'occupied': True,
        'reservationendtime': tiempo_reserva
    })
    
    return Response({'success': 'Casillero reservado con éxito'})

# Función para compartir un casillero
def compartir_casillero(request, id):
    if request.method == 'POST':
        # Obtener el nickname del usuario con quien se quiere compartir
        nickname = request.POST.get('nickname')

        # Referencia al casillero en Firebase
        ref = db.reference(f'lockers/{id}')

        # Obtener la lista actual de usuarios con los que se comparte el casillero
        casillero = ref.get()
        shared_with = casillero.get('sharedwith', [])

        # Agregar el nuevo nickname a la lista
        if nickname not in shared_with:
            shared_with.append(nickname)

        # Actualizar la base de datos
        ref.update({
            'sharedwith': shared_with
        })

        return redirect('casilleros:detalle_casillero', id=id)

    return render(request, 'casilleros/compartir.html', {'id': id})
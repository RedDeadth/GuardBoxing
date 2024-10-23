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
from rest_framework import status

@api_view(['GET'])
def casilleros_list(request):
    ref = db.reference('lockers')
    casilleros = ref.get()

    if casilleros:
        # Convierte los datos a una lista que incluye el ID
        casilleros_con_id = []
        for key, value in casilleros.items():
            value['id'] = key  # Agregar el ID basado en la clave
            casilleros_con_id.append(value)

        serializer = CasilleroSerializer(casilleros_con_id, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"message": "No hay casilleros disponibles."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def crear_casillero(request):
    serializer = CasilleroSerializer(data=request.data)

    if serializer.is_valid():
        id = serializer.validated_data['id']
        ref = db.reference(f'lockers/{id}')

        if ref.get() is not None:
            return Response({"error": "El casillero con este ID ya existe."}, status=status.HTTP_400_BAD_REQUEST)

        ref.set(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def detalle_casillero(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero:
        serializer = CasilleroSerializer(data=casillero)
        serializer.is_valid()  # Para validación en caso de que necesites
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def abrir_casillero(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Obtener el estado actual de 'open'
    open_state = casillero.get('open', False)

    # Invertir el estado de 'open'
    new_open_state = not open_state

    # Actualizar el estado en Firebase
    ref.update({'open': new_open_state})

    return Response({'open': new_open_state}, status=status.HTTP_200_OK)

@api_view(['GET'])
def gestionar_apertura(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Cambiar el estado de apertura basado en el booleano "open"
    nuevo_estado_apertura = not casillero.get('open')  # Invierte el estado actual de "open"
    ref.update({'open': nuevo_estado_apertura})

    return Response({
        'open': nuevo_estado_apertura,
        'mensaje': 'Cerrado' if not nuevo_estado_apertura else 'Abierto'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def bloquear_casillero(request, id):
    # Referencia al casillero en Firebase
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Obtener el estado actual de 'blocked'
    blocked = casillero.get('blocked', False)

    # Invertir el estado de 'blocked'
    new_blocked_state = not blocked

    if new_blocked_state:
        ref.update({
            'blocked': new_blocked_state,
            'open': False,  # Cerrar el casillero
            'userId': None  # Evitar que el usuario que lo reservó lo gestione
        })
    else:
        ref.update({'blocked': new_blocked_state})  # Solo desbloquear

    return Response({'blocked': new_blocked_state}, status=status.HTTP_200_OK)

"""
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
    """
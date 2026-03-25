from django.shortcuts import render, redirect
from firebase_admin import db, auth
from django.contrib.auth.decorators import login_required
from .utils import login_required_firebase
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
        casilleros_con_id = []
        if isinstance(casilleros, dict):
            for key, value in casilleros.items():
                value['id'] = key
                casilleros_con_id.append(value)
        elif isinstance(casilleros, list):
            for i, value in enumerate(casilleros):
                if value is not None:
                    value['id'] = str(i)
                    casilleros_con_id.append(value)

        for item in casilleros_con_id:
            uid = item.get('userId')
            if uid:
                try:
                    user_record = auth.get_user(uid)
                    item['userEmail'] = user_record.email
                    item['userName'] = user_record.display_name
                except Exception:
                    pass

        serializer = CasilleroSerializer(casilleros_con_id, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"message": "No hay casilleros disponibles."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def crear_casillero(request):
    serializer = CasilleroSerializer(data=request.data)

    if serializer.is_valid():
        id = serializer.validated_data.get('id', None)  # Verifica si el 'id' está presente en los datos validados

        if not id:
            return Response({"error": "El campo 'id' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

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
        casillero['id'] = id
        uid = casillero.get('userId')
        if uid:
            try:
                user_record = auth.get_user(uid)
                casillero['userEmail'] = user_record.email
                casillero['userName'] = user_record.display_name
            except Exception:
                pass

        serializer = CasilleroSerializer(data=casillero)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def gestionar_apertura(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    nuevo_estado_apertura = not casillero.get('open')
    ref.update({'open': nuevo_estado_apertura})

    return Response({
        'open': nuevo_estado_apertura,
        'mensaje': 'Cerrado' if not nuevo_estado_apertura else 'Abierto'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def bloquear_casillero(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    blocked = casillero.get('blocked', False)
    new_blocked_state = not blocked

    if new_blocked_state:
        ref.update({
            'blocked': new_blocked_state,
            'open': False,
            'userId': None
        })
    else:
        ref.update({'blocked': new_blocked_state})

    return Response({'blocked': new_blocked_state}, status=status.HTTP_200_OK)

@api_view(['GET'])
def abrir_casillero(request, id):
    ref = db.reference(f'lockers/{id}')
    casillero = ref.get()

    if casillero is None:
        return Response({"error": "Casillero no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    open_state = casillero.get('open', False)
    new_open_state = not open_state
    ref.update({'open': new_open_state})

    return Response({'open': new_open_state}, status=status.HTTP_200_OK)
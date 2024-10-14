from django.shortcuts import render, redirect
from firebase_admin import db
from django.contrib.auth.decorators import login_required
from .utils import login_required_firebase  # Importar el decorador personalizado

# Mostrar lista de casilleros
@login_required_firebase
def casilleros_list(request):
    ref = db.reference('casilleros')
    casilleros = ref.get()  # Obtiene todos los casilleros desde Firebase Realtime Database
    return render(request, 'casilleros/list.html', {'casilleros': casilleros})


# Crear nuevo casillero

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
            'estado': 'disponible',  # El estado puede ser 'disponible' o 'bloqueado'
        })

        return redirect('casilleros:casilleros_list')
    return render(request, 'casilleros/crear.html')

# Detalles de un casillero
def detalle_casillero(request, id):
    ref = db.reference(f'casilleros/{id}')
    casillero = ref.get()
    return render(request, 'casilleros/detalle.html', {'casillero': casillero})

def bloquear_casillero(request, id):
    ref = db.reference(f'casilleros/{id}')
    casillero = ref.get() 
    if casillero:
        # Verificar el estado actual
        if casillero['estado'] == 'desbloqueado':
            # Si está disponible, bloquearlo
            ref.update({'estado': 'bloqueado'})
        elif casillero['estado'] == 'bloqueado':
            # Si ya está bloqueado, desbloquearlo
            ref.update({'estado': 'desbloqueado'})

    return redirect('casilleros:casilleros_list')

def cambiar_estado_casillero(request, id):
    # Referencia a la ubicación del casillero en Firebase
    ref = db.reference(f'casilleros/{id}')
    casillero = ref.get()  # Obtiene el casillero con el ID

    # Verifica si el casillero existe
    if casillero:
        # Si el estado es 'abierto', lo cambia a 'cerrado', y viceversa
        nuevo_estado = 'cerrado' if casillero['estado_apertura'] == 'abierto' else 'abierto'
        ref.update({'estado_apertura': nuevo_estado})
    
    # Redirigir a la lista de casilleros
    return redirect('casilleros:casilleros_list')

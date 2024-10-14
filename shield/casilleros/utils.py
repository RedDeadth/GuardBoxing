from functools import wraps
from django.shortcuts import redirect
import firebase_admin
from firebase_admin import auth

def login_required_firebase(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si el token de Firebase está presente en la sesión
        id_token = request.session.get('id_token')
        
        if id_token:
            try:
                # Verifica el token con Firebase Admin SDK
                decoded_token = auth.verify_id_token(id_token)
                request.firebase_user = decoded_token  # Opcional, para acceder a los datos del usuario en la vista
                return view_func(request, *args, **kwargs)
            except Exception as e:
                # Si el token no es válido, redirigir al login
                print(f"Error al verificar el token: {e}")
                return redirect('login')
        else:
            # Si no hay token, redirigir al login
            return redirect('login')
    return _wrapped_view

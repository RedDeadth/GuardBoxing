from django import forms

# forms.py
    
class RegistroForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', max_length=100)
    email = forms.EmailField(label='Correo', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Verificar si las contraseñas coinciden
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Correo o Nickname', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

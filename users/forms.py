# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package users.forms
#
# Formulario correspondiente a la aplicación participación
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput
)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    """!
    Formulario de Registro

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 23-08-2017
    @version 1.0.0
    """
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder': 'Nombre de Usuario'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder': 'Repita la Contraseña'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder': 'Apellido'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Correo'})

        
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
        
class LoginForm(AuthenticationForm):
    """!
    Formulario de Logeo

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 23-08-2017
    @version 1.0.0
    """
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder': 'Nombre de Usuario'})
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder': 'Contraseña'})
        
    def clean(self):
        """!
        Método que valida si el usuario a autenticar es valido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 21-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con los errores
        """
        usuario = self.cleaned_data['username']
        contrasena = self.cleaned_data['password']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verifique su usuario o contraseña"
            self.add_error('username', msg)
        
        
class PasswordResetForm(PasswordResetForm):
    """!
    Clase del formulario de resetear contraseña

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 02-05-2017
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Correo'})

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get("email")

        if email:
            msg = "Error no existe el email"
            try:
                User.objects.get(email=email)
            except:
                self.add_error('email', msg)
                
                

class PasswordConfirmForm(SetPasswordForm):
    """!
    Formulario para confirmar la constraseña

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 15-05-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        super(PasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Contraseña Nueva'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Repita su Contraseña'})
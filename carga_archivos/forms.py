# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package carga_archivos.forms
#
# Formulario correspondiente a la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.4

from django import forms
from .models import Carga

class CargaForm(forms.ModelForm):
    
    ## Nombre del directorio
    carga_dir = forms.CharField(label=('Nombre del directorio'), widget=forms.TextInput(attrs={'class':'form-control'}))
    
    ## Instancia de los archivos
    corpus = forms.FileField(label=('Archivos'), widget=forms.ClearableFileInput(attrs={'class':'file','multiple':'multiple','type':'file'}))

    class Meta:
        model = Carga
        exclude = ['user']
        
        
class CargaUpdateForm(forms.ModelForm):
        
    ## Instancia de los archivos
    corpus = forms.FileField(label=('Archivos'), widget=forms.ClearableFileInput(attrs={'class':'file','multiple':'multiple','type':'file'}))

    class Meta:
        model = Carga
        exclude = ['carga_dir','user']
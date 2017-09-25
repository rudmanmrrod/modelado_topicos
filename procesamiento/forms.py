# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package procesamiento.forms
#
# Formulario correspondiente a la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.4


import os
from django import forms
from modelado_topicos.settings import PROCESAMIENTO_PATH
from base.functions import cargar_procesamiento, validate_dir, cargar_archivos
from .models import Procesamiento

class ProcesamientoForm(forms.ModelForm):
    """!
    Clase para crear el formulario del procesamiento
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    """
    
    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        user = kwargs.pop('user')
        super(ProcesamientoForm, self).__init__(*args, **kwargs)
        
        self.fields['carga'].choices = cargar_archivos(user.id)
        
    ## Campo con el nombre del directorio a procesar
    nombre = forms.CharField(label=('Nombre del Perfil'), widget=forms.TextInput(attrs={'class':'form-control'}))
   
    ## Palabras a excluir
    words = forms.MultipleChoiceField(label = ('Palabras'),choices = [('V', 'verbos'),('A', 'adjetivos'), ('N', 'sustantivos'),
        ('R', 'adverbios'),('D', 'determinantes'),('P', 'pronombres'),('C', 'conjunciones'),('I', 'interjecciones'),('S', 'preposiciones')],
        widget=forms.SelectMultiple(attrs={'class':'form-control'}),required=False)
    
    ## Listado de palabras excluidas por el usuario
    excluded_words = forms.CharField(label=('Palabras Excluidas'),widget=forms.TextInput(attrs={'class':'form-control','data-role':'tagsinput'}),required = False)
    
    ## Campo con el nombre del directorio a procesar
    carga = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
        label="Selecione una instacia con archivos")
        
    class Meta:
        model = Procesamiento
        exclude = ['user','consulta','used','carga']
        
        
class ProcesamientoActionForm(forms.Form):
    """!
    Clase del formulario que los perfiles de procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        user = kwargs.pop('user')
        super(ProcesamientoActionForm, self).__init__(*args, **kwargs)
        
        self.fields['procesamiento'].choices = cargar_procesamiento(user.id)

    ## Procesamientos
    procesamiento = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
        label="Selecione un perfil de procesamiento")
# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package procesamiento.models
#
# Modelos correspondientes a la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from carga_archivos.models import Carga

class Procesamiento(models.Model):
    """!
    Clase que gestiona el guardado del procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    ## Campo con el nombre del perfil de procesar
    nombre = models.CharField(max_length=30)
      
    ## Palabras a excluir
    words = models.CharField(max_length=100)
    
    ## Listado de palabras excluidas por el usuario
    excluded_words = models.CharField(max_length=500)
    
    ## Indica si fue corrido al menos una vez
    used = models.BooleanField(default=False)
    
    ## Relación con el user
    user = models.ForeignKey(User)
    
    ## Relación con la carga
    carga = models.ForeignKey(Carga)
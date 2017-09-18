# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package procesamiento.urls
#
# Urls de la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.4

from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    ## Urls del procesamiento
    url(r'^$', ProcesamientoSelect.as_view(), name = "procesamiento_select"),
    url(r'^list$', ProcesamientoList.as_view(), name = "procesamiento_index"),
    url(r'^create$', ProcesamientoCreate.as_view(), name = "procesamiento_create"),
    url(r'^delete/(?P<pk>\d+)$', ProcesamientoDelete.as_view(), name = "procesamiento_delete"),
    url(r'^update/(?P<pk>\d+)$', ProcesamientoUpdate.as_view(), name = "procesamiento_update"),
]

## Urls por ajax
urlpatterns += [
    url(r'^ajax/validar_procesamiento/?$', validar_procesamiento, name='validar_procesamiento_nid'),
    url(r'^ajax/validar_procesamiento/(?P<pk>\d+)$', validar_procesamiento, name='validar_procesamiento'),
]
# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package carga_archivos.urls
#
# Urls de la aplicación carga_archivos
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.4
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^crear$', CreateCargaArchivos.as_view(), name = "carga_archivos_create"),
    url(r'^listar$', ListCargaArchivos.as_view(), name = "carga_archivos_list"),
    url(r'^actualizar/(?P<pk>\d+)$', UpdateCargaArchivos.as_view(), name = "carga_archivos_update"),
    url(r'^borrar/(?P<pk>\d+)$', DeleteCargaArchivos.as_view(), name = "carga_archivos_delete"),
]

## Urls por ajax
urlpatterns += [
]
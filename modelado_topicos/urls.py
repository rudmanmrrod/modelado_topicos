# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package modelado_topicos.urls
#
# Urls base de la aplicación
# @author Generated by 'django-admin startproject' using Django 1.11.
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.4

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('base.urls')),
    url(r'^', include('users.urls')),
    url(r'^visualizacion/', include('visualization.urls')),
    url(r'^procesamiento/', include('procesamiento.urls')),
    url(r'^carga-archivos/', include('carga_archivos.urls')),
]

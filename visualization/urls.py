# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package visualiztion.urls
#
# Urls de la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^topics.json/(?P<id>\d+)/(?P<k>\d+)/$', topics , name='topics'),
    url(r'^topic/(?P<id>\d+)/(?P<k>\d+)/(?P<topic_no>\d+)/$', visualize , name='visualize'),
    url(r'^doc/(?P<id>\d+)/(?P<k>\d+)/(?P<filename>.+)/$', visualize , name='visualize_doc'),
    url(r'^see_doc/(?P<id>\d+)/(?P<k>\d+)/(?P<propuesta>.+)/$',VerDocumento.as_view(),name='see_doc'),
    url(r'^list_topics/(?P<id>\d+)/$', ListTopics.as_view() , name='list_topic'),
]

## Urls por ajax
urlpatterns += [
    url(r'^topics/(?P<id>\d+)/(?P<k>\d+)/(?P<topic_no>\d+)/$', topic_json , name='topic_json'),
    url(r'^docs_topics/(?P<id>\d+)/(?P<k>\d+)/(?P<doc_id>.+)/$', doc_topics , name='doc_topics'),
    url(r'^generate_topics/(?P<id>\d+)/(?P<k>\d+)$', generate_topics , name='generate_topics'),
]
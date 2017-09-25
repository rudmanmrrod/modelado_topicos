# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package base.functions
#
# Funciones génericas de la aplicación
# @author Generated by 'django-admin startproject' using Django 1.11.
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.4
import os
from procesamiento.models import Procesamiento
from carga_archivos.models import Carga
from modelado_topicos.settings import PROCESAMIENTO_PATH

def cargar_procesamiento(pk=None):
    """!
    Función que permite cargar los procesamientos

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @return Devuelve una tupla con los perfiles de procesamiento
    """

    lista = ('', 'Seleccione...'),

    Pro = Procesamiento.objects.filter(user_id=pk) if pk else Procesamiento.objects
    try:
        for procesamiento in Pro.all():
            lista += (procesamiento.id, procesamiento.nombre),
    except Exception as e:
        pass

    return lista

def cargar_archivos(pk=None):
    """!
    Función que permite cargar las intancias de carga que haya realizado un usuario

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 25-08-2017
    @return Devuelve una tupla con los perfiles de procesamiento
    """

    lista = ('', 'Seleccione...'),

    Cargas = Carga.objects.filter(user_id=pk) if pk else Procesamiento.objects
    try:
        for carga in Cargas.all():
            lista += (carga.id, carga.carga_dir),
    except Exception as e:
        pass

    return lista


def createPreprocessingFiles(id):
    """!
    Crea los archivos necesarios del preprocesamiento a partir de las respuestas
    abiertas de una consulta.

    La función creará el directorio consulta_publica/static/procesamiento_files/nombre_consulta/orig
    con un conjunto de archivos de texto que representan cada una de las repuestas
    abiertas de la consulta. Por ejemplo:
    .
    miconsulta
    |---orig
        |--- respuesta_5.txt
        |--- respuesta_6.txt

    En caso de existir el directorio al momento de ejecutarse esta función será
    borrado.

    @author Antonio Araujo  (aaraujo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param id Identificador de la consulta para obtener respuestas abiertas
    """

    try:
        # obtener la consulta con id pasado como argumento
        consulta = Consulta.objects.get(id=id)
        
        ## Se crea un nombre sin espacios en blanco
        nombre = "_".join(consulta.nombre_consulta.split(" "))

        # crear un directorio con el nombre de la consulta en consulta_publica/static/procesamiento_files/
        processingDirectory = PROCESAMIENTO_PATH + '/' + nombre + '/orig'

        # borrar directorio en el caso de existir
        if os.path.isdir(processingDirectory) :
            shutil.rmtree(processingDirectory)
        os.makedirs(processingDirectory)

        # obtener las preguntas
        for pregunta in Pregunta.objects.filter(consulta_id=consulta.id).all() :
            if pregunta.tipo_pregunta_id==5 :
                # ubicar la respuesta
                for respuesta in RespuestaAbierta.objects.filter(pregunta_id=pregunta.id).all():
                    # escribir archivo a disco
                    filePath = processingDirectory + '/' + 'respuesta_' + str(respuesta.id)+".txt"
                    fo = open(filePath, "w")
                    fo.write(respuesta.texto_respuesta.encode('utf8'));
                    fo.close()
        
        return True

    except Exception as e:
        print "La consulta con identificado "+ str(id) + " no existe"
        print e
        return False
        pass
    
def validate_dir(pk):
    """!
    Función que permite cargar las consultas con directorios creados

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 17-04-2017
    @param pk {int} Recibe id de la consulta
    @return Devuelve una tupla con las consultas que tienen directorios
    """
    
    consulta = Consulta.objects.filter(pk=pk)
    if consulta:
        consulta = consulta.get()
        nombre = "_".join(consulta.nombre_consulta.split(" "))
        consulta_dir = PROCESAMIENTO_PATH+"/"+nombre
        if os.path.exists(consulta_dir):
            return True
        return False
    else:
        return False
    
def dump_exception():
    """!
    Función para captar los errores e imprimirlos

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @return Retorna una respuesta http con el error
    """
    import sys,traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print ("*** print_exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    return HttpResponseServerError(str(exc_value))

def validar_directorio_procesamiento(pk):
    """!
    Función que permite validar si ya se ejecutó el procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 18-09-2017
    @param pk {int} Recibe id del perfil de procesamiento
    @return Devuelve un booleano
    """
    procesamiento = Procesamiento.objects.get(pk=pk)
    procesamiento_dir = PROCESAMIENTO_PATH+"/"+procesamiento.carga.carga_dir
    
    if not os.path.exists(procesamiento_dir):
        return False
    if not os.path.exists(procesamiento_dir+"/orig"):
        return False
    elif len(os.listdir(procesamiento_dir+"/orig"))==0:
        return False
    if not os.path.exists(procesamiento_dir+"/lower"):
        return False
    elif len(os.listdir(procesamiento_dir+"/lower"))==0:
        return False
    if not os.path.exists(procesamiento_dir+"/noaccent"):
        return False
    elif len(os.listdir(procesamiento_dir+"/noaccent"))==0:
        return False
    if not os.path.exists(procesamiento_dir+"/freeling"):
        return False
    elif len(os.listdir(procesamiento_dir+"/freeling"))==0:
        return False
    if not os.path.exists(procesamiento_dir+"/pp"):
        return False
    elif len(os.listdir(procesamiento_dir+"/pp"))==0:
        return False
    if os.path.exists(procesamiento_dir+"/lda"):
        if not os.path.exists(procesamiento_dir+'/lda/corpus.dat') or not os.path.exists(procesamiento_dir+'/lda/vocab.txt'):
            return False
        elif len(os.listdir(procesamiento_dir+"/lda"))<11:
            return False
    else:
        return False
    return True

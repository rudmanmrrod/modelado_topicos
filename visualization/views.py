# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package visualiztion.views
#
# Vistas de la aplicación de Visualization
# @author Generated by 'django-admin startproject' using Django 1.11.
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.4
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
## Requirimientos del modelado de tópicos
from base.functions import dump_exception
from modelado_topicos.settings import PROCESAMIENTO_PATH
from procesamiento.models import Procesamiento
from utils.ldac2vsm import *
from utils.json_data import *
from vsm.viewer.ldagibbsviewer import LDAGibbsViewer as LDAViewer

def topic_json(request,id,k,topic_no, N=40):
    """!
    Función para retornar la data de los tópicos en json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param k <b>{int}</b> Recibe el número de tópicos a mostrar
    @param topic_no <b>{string}</b> Recibe el número de tópicos
    @param N <b>{int}</b> Recibe la cantidad
    @return Retorna el render de la vista
    """
    k_param, lda_c, lda_m, lda_v = '','','',''
    try:
        if k != k_param:
            k_param = k
            lda_v = generate_topic(id,k_param,lda_c,lda_m,lda_v)
        try:
            N = int(request.query.n)
        except:
            pass

        if N > 0:
            data = lda_v.dist_top_doc([int(topic_no)])[:N]
        else:
            data = lda_v.dist_top_doc([int(topic_no)])[N:]
            data = reversed(data)

        docs = [doc for doc,prob in data]
        doc_topics_mat = lda_v.doc_topics(docs)

        js = []
        for doc_prob, topics in zip(data, doc_topics_mat):
            doc, prob = doc_prob
            js.append({'doc' : doc, 'label': label(doc), 'prob' : 1-prob,
                'topics' : dict([(str(t), p) for t,p in topics])})
        return JsonResponse(js,safe=False)
    except:
        return dump_exception()
    
def visualize(request,id,k,filename=None,topic_no=None):
    """!
    Función para visualizar los tópicos

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param k <b>{int}</b> Recibe el número de tópicos a mostrar
    @param filename <b>{string}</b> Recibe el nombre del  archivo
    @param topic_no <b>{int}</b> Recibe el número de tópico
    @return Retorna el render de la vista
    """
    k_param, lda_c, lda_m, lda_v = '','','',''
    try:
        if k != k_param:
            k_param = k
            lda_v = generate_topic(id,k_param,lda_c,lda_m,lda_v)
        template_name = 'visualization.index.html'
        return render(request,template_name,
            {'k_param':k_param,
             'topic_no':topic_no,
             'filename':filename,
             'id' : id,
             'topics_range' : [10,20,30,40,50,60,70,80,90],
            })
    except:
        return dump_exception()
    
    
def topics(request,id,k):
    """!
    Función para servir los tópicos como un json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param id <b>{int}</b> Id del procesamiento
    @param k <b>{int}</b> Número de tópicos
    @return Retorna el objeto json
    """
    lda_c,lda_m,lda_v = '','',''
    lda_v = generate_topic(id,k,lda_c,lda_m,lda_v)
    try:
        js=populateJson(lda_v)
        return JsonResponse(js,safe= False)
    except:
        return dump_exception()
    
    
def doc_topics(request,id,k,doc_id, N=40):
    """!
    Función para retornar la data de los documentos en json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param id <b>{int}</b> Id del procesamiento
    @param doc_id <b>{string}</b> Recibe el número del documento
    @param N <b>{int}</b> Recibe la cantidad
    @return Retorna el render de la vista
    """
    lda_c,lda_m,lda_v = '','',''
    try:
        lda_v = generate_topic(id,k,lda_c,lda_m,lda_v)
        try:
            N = int(request.query.n)
        except:
            pass
        js = doc_json(lda_v,doc_id,N)
        return JsonResponse(js,safe=False)
    except:
        return dump_exception()
    
def generate_topic(id,k_param,lda_c,lda_m,lda_v):
    """!
    Función para generar los tópicos

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 13-03-2017
    @param id <b>{int}</b> Contiene el id del procesamiento
    @param k_param <b>{int}</b> Contiene la cantidad de tópicos
    @param lda_c <b>{object}</b> Objeto que perteneciente al lda
    @param lda_m <b>{object}</b> Objeto que perteneciente al lda
    @param lda_v <b>{object}</b> Objeto que perteneciente al lda
    """
    procesamiento = Procesamiento.objects.get(pk=id)
    dir_consulta = procesamiento.carga.carga_dir
    LDA_DATA_PATH = PROCESAMIENTO_PATH + '/' + dir_consulta+'/lda/'+dir_consulta+'{0}/'
    LDA_CORPUS_FILE = PROCESAMIENTO_PATH + '/' + dir_consulta+'/lda/corpus.dat'
    LDA_VOCAB_FILE = PROCESAMIENTO_PATH + '/' + dir_consulta+'/lda/vocab.txt'
    LDA_CORPUS_DIR = PROCESAMIENTO_PATH + '/' + dir_consulta+'/pp/'
    lda_c,lda_m = corpus_model(k_param,LDA_DATA_PATH.format(k_param),
                       LDA_CORPUS_FILE,
                       LDA_VOCAB_FILE,
                       LDA_CORPUS_DIR)
    lda_v = LDAViewer(lda_c, lda_m)
    return lda_v


class VerDocumento(LoginRequiredMixin,TemplateView):
    """!
    Clase que permite la visualización de un archivo en particular
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 30-03-2017
    """
    
    template_name='visualization.docs.html'
    
    
    def get(self, request, id, k, propuesta = None):
        """!
        Metodo que permite procesar las peticiones por get, con el fin de mostrar el documento
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 31-07-2015
        @param self <b>{object}</b> Objeto que instancia el método
        @param request <b>{object}</b> Objeto que mantiene la peticion
        @param propuesta <b>{int}</b> Recibe el número de la propuesta
        @return Retorna el render de la vista
        """
        lda_c,lda_m,lda_v = '','',''
        lda_v = generate_topic(id,k,lda_c,lda_m,lda_v)
        #Obtnener json
        Topic_Json = populateJson(lda_v)
        Topic_Json = json.dumps(Topic_Json)
        topicos = json.loads(Topic_Json)
        N = len(topicos)
        Docs = doc_json(lda_v,propuesta,N)
        Docs = json.dumps(Docs)
        documentos = self.obtenerDocumento(json.loads(Docs),propuesta)
        documentos = json.dumps(documentos)
        mi_color = []
        mi_color = self.obtenerValores(topicos)
        mi_color = json.dumps(mi_color)
        topicos = json.dumps(topicos)
        ## Se carga el perfil
        procesamiento = Procesamiento.objects.get(pk=id)
        dir_consulta = procesamiento.carga.carga_dir
        files = PROCESAMIENTO_PATH + '/' + dir_consulta+'/noaccent/'
        #carga el pre-procesado del archivo en una variable
        texto=''
        direccion = files + '/'+ propuesta
        try:
            archivo = open(direccion,'r')
            texto=archivo.read()
            archivo.close()
        except:
            return dump_exception()
            texto='No se encontro el documento'
        return render(request,self.template_name,
                      {'topicos':topicos,
                       'propuesta':propuesta,
                       'color':mi_color,
                       'texto':texto,
                       'documento':documentos})
    
    def obtenerValores(self,topicos):
        """!
        Metodo para obtener los colores del json
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 31-07-2015
        @param self <b>{object}</b> Objeto que instancia el método
        @param topicos <b>{dict}</b> Recibe un diccionario con los topicos 
        @return Retorna un diccionario con los colores
        """
        my_topic=[]
        for x in topicos:
            my_topic.append(topicos[x]['color'])
        return my_topic
    
    def obtenerDocumento(self,docs,propuesta):
        """!
        Metodo para obtener un documento
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 03-02-2016
        @param self <b>{object}</b> Objeto que instancia el método
        @param docs <b>{dict}</b> Recibe un diccionario con los documentos
        @param propuesta <b>{int}</b> Recibe el número de la propuesta
        @return Retorna un diccionario con los colores
        """
        for x in docs:
            if(x['doc']==propuesta):
                return x
            
            
class ListTopics(LoginRequiredMixin,TemplateView):
    """!
    Clase que permite la visualización de un archivo en particular
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 30-03-2017
    """
    
    template_name='visualization.topics.list.html'
    
    def get_context_data(self,**kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 30-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['topics_range'] = [10,20,30,40,50,60,70,80,90]
        kwargs['id'] = self.kwargs['id']
        return super(ListTopics, self).get_context_data(**kwargs)
    
def generate_topics(request,id,k):
    """!
    Metodo que genera una lista de los tópicos dado un párametro k

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 30-03-2017
    @param request <b>{object}</b> Recibe la peticion
    @param id <b>{int}</b> Id del procesamiento
    @param k <b>{int}</b> Número de tópicos
    @return Retorna el json con las subunidades que consiguió
    """
    lda_c,lda_m,lda_v = '','',''
    if(int(k) in [10,20,30,40,50,60,70,80,90]):
        lda_v = generate_topic(id,k,lda_c,lda_m,lda_v)    
        js = populateJson(lda_v)
        return JsonResponse(js,safe=False)
    return JsonResponse("El párametro k es inválido",safe=False)
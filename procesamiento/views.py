# -*- coding: utf-8 -*-
"""
Sistema de modelado de Tópicos v1.4

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package procesamiento.views
#
# Vistas correspondientes a la aplicación procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.4

from shutil import copy, rmtree
from django.shortcuts import render
from django.views.generic import (
    FormView, TemplateView, CreateView, ListView,
    DeleteView, UpdateView
    )
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
## Importaciones de la consulta
from modelado_topicos.settings import PROCESAMIENTO_PATH, BASE_DIR
## Importaciones propias
from .forms import ProcesamientoForm, ProcesamientoActionForm
from .models import Procesamiento
from base.functions import validar_directorio_procesamiento
from carga_archivos.models import Carga
## Importaciones de los utils
from modelado_topicos.settings import BASE_DIR
from utils.freeling import *
from utils.corpusScript import *
from utils.run_lda import generate_comand


class ProcesamientoSelect(LoginRequiredMixin,FormView):
    """!
    Clase que gestiona la vista principal de las opciones del procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    template_name = "procesamiento.select.html"
    form_class = ProcesamientoActionForm
    
    def get_form_kwargs(self,**kwargs):
        """!
        Metodo que permite pasar el id de la consulta y pasarlo al form
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 17-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el id de la consulta
        """
        kwargs = super(ProcesamientoSelect, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
        
    def get_context_data(self, **kwargs):
        """!
        Metodo para cargar/obtener valores en el contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        procesamiento = Procesamiento.objects.filter(user_id=self.request.user.id)
        if(procesamiento):
            kwargs['procesamiento'] = True
        return super(ProcesamientoSelect, self).get_context_data(**kwargs)
    
    def form_valid(self,form):
        """!
        Metodo que permite procesar si el formulario es válido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 29-03-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param form <b>{object}</b> Objeto que contiene el formulario
        @return Retorna un redirect a la success_url
        """
        ## Variable para determinar si se hace o no el freeling
        make_freeling = True
        
        procesamiento_id  = form.cleaned_data['procesamiento']
        
        no_freeling = self.request.GET.get('no_freeling','')
        
        if(no_freeling=='True'):
            make_freeling = False
        
        procesamiento = Procesamiento.objects.get(pk=procesamiento_id)
        excluded_words = procesamiento.excluded_words
        
        if len(excluded_words)>0:
            excluded_words = [item.strip() for item in excluded_words.split(",")]
                   
        ## Se crea el directorio del procesamiento
        procesamiento_dir = PROCESAMIENTO_PATH+"/"+procesamiento.carga.carga_dir
            
        ## Se preparan los archivos/directorios necesarios para el pre-procesamiento
        self.prepare_files(procesamiento_dir)
        
        ## Se realiza el freeling y procesamiento con LDA
        self.make_process(procesamiento_dir, make_freeling, procesamiento.words,procesamiento.excluded_words)
        
        ## Se guarda como corrido el procesamiento
        procesamiento.used = True
        procesamiento.save()
        
        ## Se crea el mensaje
        messages.info(self.request,"Se finalizó el procesamiento con éxito")
        
        if self.request.is_ajax():
            return JsonResponse({"code":True})
        else:
            return super(ProcesamientoSelect, self).form_valid(form)
        
    def prepare_files(self,dest):
        """!
        Metodo para copiar los corpus del destino al origen y crear los directorios
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 08-02-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param dest <b>{str}</b> Recibe la ruta de destino
        """
        ## Se crean los directorios necesarios para el pre-procesamiento
        if not os.path.exists(dest+"/lower/"):
            os.mkdir(dest+"/lower/")
        if not os.path.exists(dest+"/pp/"):
            os.mkdir(dest+"/pp/")
        if not os.path.exists(dest+"/lda/"):
            os.mkdir(dest+"/lda/")
        if not os.path.exists(dest+"/freeling/"):
            os.mkdir(dest+"/freeling/")
        if not os.path.exists(dest+"/noaccent/"):
            os.mkdir(dest+"/noaccent/")
            
    def make_process(self, path, make_freeling, word_list ,exluded_words):
        """!
        Metodo para realizar el pre-procesamiento y lda
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-02-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param path <b>{str}</b> Recibe la ruta de origen del corpus
        @param make_freeling <b>{bool}</b> Recibe si desea ejecutar el freeling
        @param word_list <b>{list}</b> Recibe una lista palabras a excluir
        @param exluded_words <b>{list}</b> Recibe una lista de las palabras a excluir
        """
        orig_corpus_path = path + '/orig/'
        lower_corpus_path = path + '/lower/'
        pp_corpus_path = path + '/pp/'
        lda_corpus_path = path + '/lda/'
        
        ## Crea los archivos de puro minusculas
        files_to_lower(orig_corpus_path,lower_corpus_path)
        
        ## Se realiza el pre-procesamiento
        if len(word_list)>1:
            file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=make_freeling,pos_list=word_list)
        else:
            file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=make_freeling)
        
        ## Se genera el archivo de vocabulario excluido
        generate_exluded_file(path+"/",pp_corpus_path,file_words_pp,exluded_words)
        
        ## Se generan los archivos .dat
        corpus_script(pp_corpus_path,lda_corpus_path)
        
        ## Se generan los archivos con el LDA
        corpus_dat = lda_corpus_path+'corpus.dat' 
        generate_comand(BASE_DIR,corpus_dat,path,9)
    
class ProcesamientoCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    """!
    Clase que gestiona la creación de perfiles procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    model = Procesamiento
    form_class = ProcesamientoForm
    template_name = "procesamiento.create.html"
    success_message = "Se creó el perfil de procesamiento con éxito"
    success_url = reverse_lazy('procesamiento_index')
    
    def get_form_kwargs(self):
        """!
        Metodo que permite guardar el usuario en los kwargs
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 25-08-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el username
        """
        kwargs = super(ProcesamientoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    
    def form_valid(self,form):
        """!
        Metodo que al que accede si el formulario es válido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        carga = Carga.objects.get(pk=form.cleaned_data['carga'])
        user = User.objects.get(pk=self.request.user.id)
        self.object = form.save(commit=False)
        self.object.nombre = form.cleaned_data['nombre']
        self.object.words = form.cleaned_data['words']
        self.object.excluded_words = form.cleaned_data['excluded_words']
        self.object.carga = carga
        self.object.user = user
        self.object.save()
        return super(ProcesamientoCreate, self).form_valid(form)
    
    
class ProcesamientoList(LoginRequiredMixin,ListView):
    """!
    Clase que gestiona la lista de los perfiles procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    model = Procesamiento
    template_name = "procesamiento.list.html"
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        """!
        Metodo para cargar/obtener valores en el contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 28-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        context = super(ProcesamientoList, self).get_context_data(**kwargs)
        context['object_list'] = Procesamiento.objects.filter(user_id=self.request.user.id).all()
        ## Implementación del paginador
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return context
        
    
    
class ProcesamientoDelete(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    """!
    Clase que gestiona la borrado de perfiles de procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    model = Procesamiento
    template_name = "procesamiento.delete.html"
    success_message = "Se eliminó el perfil de procesamiento con éxito"
    success_url = reverse_lazy('procesamiento_index')
    
    
class ProcesamientoUpdate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    """!
    Clase que gestiona la actualización de perfiles de procesamiento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 28-03-2017
    @version 1.0.0
    """
    model = Procesamiento
    form_class = ProcesamientoForm
    template_name = "procesamiento.update.html"
    success_message = "Se actualizó el perfil de procesamiento con éxito"
    success_url = reverse_lazy('procesamiento_index')
    
    def get_initial(self):
        """!
        Metodo que permite cargar datos iniciales en el formulario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-09-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los datos iniciales
        """
        initial = super(ProcesamientoUpdate, self).get_initial()
        initial['carga'] = self.object.carga_id
        return initial

    def get_form_kwargs(self,**kwargs):
        """!
        Metodo que permite pasar el id de la consulta y pasarlo al form
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 17-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el kwargs con el id de la consulta
        """
        kwargs = super(ProcesamientoUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
def validar_procesamiento(request,pk):
    """!
    Función que permite validar el procesamiento vía ajax

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 18-09-2017
    @param pk {int} Recibe id del perfil de procesamiento
    @return Retorna la respuesta en Json
    """
    procesamiento = Procesamiento.objects.filter(pk=pk)
    if procesamiento:
        texto = ''
        respuesta = validar_directorio_procesamiento(pk)
        if not respuesta:
            texto = 'No ha ejecutado el procesamiento'
        else:
            texto = 'Ya ha ejecutado el procesamiento, si añadió nuevos archivos puede correr el freeling, si desea eliminar algunas\
                    palabras, no es necesario que lo ejecute'
        return JsonResponse({'resultado': respuesta,'texto':texto})
    return JsonResponse({'resultado': False,'texto':'El perfil no existe'})
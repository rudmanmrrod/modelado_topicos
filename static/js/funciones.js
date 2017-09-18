/**
 * Función para traer el listado de tópicos
 * @param {object} element Recibe el elemento
 * @param {object} event Recibe el evento
 * @param {int} id Recibe el id del procesamiento
 */
function visualize(element,event,id) {
    event.preventDefault();
    $('#status').show(500);
    var text = $(element).text();
    var number = text.split(" ")[0]
    $('#visualize').text(text);
    var url = '/visualizacion/generate_topics/'+id+"/"+number;
    $.get(url,function(data){
        if (data) {
            $('#topicos').html('');
            $.each(data,function(index,value){
                var words_ordered = Object.keys(value.words).sort(function(a,b){return value.words[b]-value.words[a];});
                var html = "<div class='panel panel-default'>";
                var url = '/visualizacion/topic/'+id+'/'+number+'/'+index;
                html += "<div class='panel-heading' style='background-color:"+value.color+"'>";
                html += "Tópico #"+index;
                html += "</div><div class='panel-body'>";
                html += words_ordered.join(", ");
                html += "</div><div class='panel-footer'>";
                html += "<a type='button' class='btn btn-default' href='"+url+"'>Ver Documentos para Tópico #"+index+"</a>"
                html += "</div></div>";
                $('#topicos').append(html);
                $('#status .progress-bar').addClass('progress-bar-success').css("width","100%").attr("aria-valuenow","100").text("Completado!");
            });
            $('#status').hide(2000);
        }
        else
        {
            $('#status .progress-bar').removeClass('active progress-bar-striped').text('No se pudieron cargar los tópicos.');
        }
    });
}

/*
 * Función para crear el pre-procesamiento por ajax
 * @param {object} form Recibe el formulario
 */
function createPreprocess(form) {
    bootbox.alert("Se le notifcará cuando finalice el pre-procesamiento");
    $.ajax({ // create an AJAX call...
        data: $(form).serialize(), // get the form data
        type: $(form).attr('method'), // GET or POST
        url: $(form).attr('action'), // the file to call
        success: function(response) { // on success..
            if (response.code) {
                //bootbox.alert("Se finalizó con éxito");
            }
            else{
                $('.container').html(response);
            }
        }
    });
}

/*
 * Función para validar el directorio de procesamiento
 * vía ajax
 * @param {object} form Recibe el formulario
 * @param {pk} int Recibe el id del perfil de procesamiento
 */
function validar_procesamiento(form,pk) {
    var url = URL_VALIDAR_PROCESAMIENTO+'/'+pk;
    $.get(url,function(data){
        if(!data.resultado){
            createPreprocess(form);
        }
        else{
            var html = data.texto;
            html += "<br/>¿Desea ejecutar de nuevo el freeling para el procesamiento?";
            bootbox.dialog({
                message: html,
                title: "Confirmación",
                buttons: {
                    success: {
                        label: "Si",
                        className: "btn-success",
                        callback: function() {
                            createPreprocess(form);
                        }
                    },
                    close: {
                        label: "No",
                        className: "btn-danger",
                        callback: function() {
                            $(form).attr('action',$(form).attr('action')+"?no_freeling=True");
                            createPreprocess(form);
                        }
                    }
                }
            });
        }
    });
}
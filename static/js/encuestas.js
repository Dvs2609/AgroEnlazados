$(document).ready(function() {
    function submitForm(formClass, url) {
        const form = $(formClass);
        const data = form.serialize();
        const modal = form.closest('.modal');
      
        $.post(url, data)
          .done(function (response) {
            if (response.result === 'success') {
              alert('Encuesta guardada con éxito.');
              modal.modal('hide');
              form.trigger('reset');
              $('body').removeClass('modal-open');
              $('.modal-backdrop').remove();
            } else {
              alert('Hubo un error al guardar la encuesta. Por favor, inténtalo de nuevo.');
            }
          })
          .fail(function () {
            alert('Hubo un error al guardar la encuesta. Por favor, inténtalo de nuevo.');
          });
    }

    $('.submit-encuestaComunicacionModal-form').on('click', function() {
        submitForm('.encuestaComunicacionModal-form', '/encuestas/comunicacion/');
    });

    $('.submit-encuestaRegistroVentaDirectaModal-form').on('click', function() {
        submitForm('.encuestaRegistroVentaDirectaModal-form', '/encuestas/registro_venta_directa/');
    });

    $('.submit-encuestaMercadillosModal-form').on('click', function() {
        submitForm('.encuestaMercadillosModal-form', '/encuestas/satisfaccion_mercadillos/');
    });
});

$('.modal').on('hidden.bs.modal', function () {
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
  });
  
// Este script actualiza el select de horarios en el admin de CitaMedica al cambiar la fecha
(function() {
    var $ = window.jQuery || window.django && window.django.jQuery;
    if (!$) return;
    $(document).ready(function() {
        var fechaInput = $('#id_fecha');
        var horaSelect = $('#id_hora_cita');
        if (!fechaInput.length || !horaSelect.length) return;
        fechaInput.on('change', function() {
            var fecha = $(this).val();
            if (!fecha) return;
            $.ajax({
                url: '/admin/doctor/horarios-disponibles/',
                data: { fecha: fecha },
                success: function(data) {
                    console.log('Horarios recibidos:', data); // <-- LOG para depuración
                    horaSelect.empty();
                    if (data.horarios && data.horarios.length > 0) {
                        horaSelect.append($('<option>', {value: '', text: 'Seleccione una hora'}));
                        data.horarios.forEach(function(hora) {
                            horaSelect.append($('<option>', {value: hora, text: hora}));
                        });
                    } else {
                        horaSelect.append($('<option>', {value: '', text: 'No hay horarios disponibles'}));
                    }
                },
                error: function() {
                    horaSelect.empty();
                    horaSelect.append($('<option>', {value: '', text: 'Error al cargar horarios'}));
                }
            });
        });
    });
})();

// admin_horarios.js
(function() {
    function updateHorasRadios() {
        var fechaInput = document.querySelector('input[name="fecha"]');
        var radiosDiv = document.getElementById('id_hora_cita_radios');
        if (!fechaInput || !radiosDiv) return;
        var fecha = fechaInput.value;
        if (!fecha) {
            radiosDiv.innerHTML = '<span style="color:#888;">Seleccione una fecha</span>';
            return;
        }
        fetch('/doctor/horarios_radios_ajax/?fecha=' + fecha)
            .then(response => response.json())
            .then(data => {
                radiosDiv.innerHTML = data.html;
            });
    }
    document.addEventListener('DOMContentLoaded', function() {
        var fechaInput = document.querySelector('input[name="fecha"]');
        if (fechaInput) {
            fechaInput.addEventListener('change', updateHorasRadios);
            updateHorasRadios();
        }
    });
})();

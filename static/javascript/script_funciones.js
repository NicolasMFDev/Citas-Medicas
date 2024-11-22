$(document).ready(function() {
    $('#especialidad').change(function() {
        var option = $(this).val();
        $.post('/proceso', {especialida: option}, function(data) {
            $('#medicos').empty();
            $('#medicos').append($('<option>Selecciona un Medico</option>').val('Seleccione'));
            $.each(data, function(index, value) {
                $('#medicos').append($('<option></option>').val(value).text(value));
            });
        });
    });
});

function mostrarCamposActualizar() {
    const consulta = document.getElementById('consulta').value;
    if (consulta) {
        fetch(`/proceso_actualizar?id=${consulta}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('nombre').value = data.nombre;
                    document.getElementById('celular').value = data.celular;
                    document.getElementById('email').value = data.email;
                    document.getElementById('form-actual').classList.remove('oculto');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function ActualizarMedico() {
    const consulta = document.getElementById('consulta').value;
    if (consulta) {
        fetch(`/proceso_medico?id=${consulta}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('nombre').value = data.nombre;
                    document.getElementById('celular').value = data.celular;
                    document.getElementById('especialidad').value = data.especialidad;
                    document.getElementById('form-actual').classList.remove('oculto');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function mostrarAlertaCancelar() {
    alert("Cita Cancelada Exitosamente!!");
    return true;
}

function mostrarAlertaActualizarBorrarPaciente() {
    const action = document.activeElement.value;
    if (action === 'actualizar') {
        alert("Paciente Actualizado Exitosamente!!");
        return true;
    }
    
    if (action === 'borrar') {
        alert("Paciente Borrado Exitosamente!!");
        return true;
    }
}

function mostrarAlertaActualizarBorrarMedico() {
    const action = document.activeElement.value;
    if (action === 'actualizar') {
        alert("Medico Actualizado Exitosamente!!");
        return true;
    }
    
    if (action === 'borrar') {
        alert("Medico Borrado Exitosamente!!");
        return true;
    }
}

async function validarAgenda(event) {
    event.preventDefault();

    const medico = document.getElementById('medicos').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;
    const fechaHora = `${fecha} ${hora}`;

    try {
        const response = await fetch(`/proceso_agendar_cita?medico=${medico}&fecha_hora=${fechaHora}`);
        const result = await response.json();

        if (result.exists) {
            alert("Esa fecha ya esta ocupada, por favor ingrese otra!!");
        } else {
            alert("Cita agendada exitosamente")
            const form = document.getElementById('agenda');
            form.submit();
        }
    } catch (error) {
        console.error('Error', error);
        alert("Ocurrio un error al verificar la fecha y hora");
    }
}

async function validarMover(event) {
    event.preventDefault();
    const citas = document.getElementById('citas').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;
    const fechaHora = `${fecha} ${hora}`;
    
    try {
        
        const response = await fetch(`/proceso_mover_cita?medico=${citas}&fecha_hora=${fechaHora}`);
        const result = await response.json();

        if (result.exists) {
            alert("Esa fecha ya esta ocupada, por favor ingrese otra!!");
        } else {
            alert("Cita Movida exitosamente")
            const form = document.getElementById('move');
            form.submit();
        }
    } catch (error) {
        console.error('Error', error);
        alert("Ocurrio un error al verificar la fecha y hora");
    }
}


$(document).ready(function() {
    $('#agregar_paciente').on('submit', function(event) {
        event.preventDefault();

        const paciente = $('#id').val();

        $.ajax({
            url: `/verificar_paciente`,
            type: 'GET',
            data: { id: paciente },
            success: function(response) {
                if (response.exists) {
                    alert("El paciente con esa identificación ya existe");
                } else {
                    $ajax({
                        url: `/agregar_paciente`,
                        type: 'POST',
                        data: $('#agregar_paciente').serialize(),
                        success: function(data) {
                            alert("Paciente Agregado Exitosamente");
                            window.location.href = '/agregar_paciente';
                        },
                        error: function(error) {
                            alert("Error al agregar el paciente");
                        }
                    });
                }
            },
            error: function(error) {
                alert("Ocurrio un error al agregar el paciente");
            }
        });
    });
});


$(document).ready(function() {
    $('#agregar_medico').on('submit', function(event) {
        event.preventDefault();

        const medico = $('#id').val();

        $.ajax({
            url: `/verificar_medico`,
            type: 'GET',
            data: { id: medico },
            success: function(response) {
                if (response.exists) {
                    alert("El medico con esa identificación ya existe");
                } else {
                    $ajax({
                        url: `/agregar_medico`,
                        type: 'POST',
                        data: $('#agregar_medico').serialize(),
                        success: function(data) {
                            alert("Medico Agregado Exitosamente");
                            window.location.href = '/agregar_medico';
                        },
                        error: function(error) {
                            alert("Error al agregar el medico");
                        }
                    });
                }
            },
            error: function(error) {
                alert("Ocurrio un error al agregar al medico");
            }
        });
    });
});
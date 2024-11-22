from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita

hospital = Hospital()

hospital.cargar_pacientes_desde_csv('data/pacientes.csv') 
hospital.cargar_medicos_desde_json('data/medicos.json') 
hospital.cargar_citas_desde_csv('data/citas.csv')      

main = Blueprint('main', __name__)

# Ruta principal
@main.route('/')
def index():
    return render_template('index.html')


# Rutas para las Citas: Consultar paciente, Agendar cita, Cancelar cita y Mover cita
@main.route('/consultar_cita', methods=['GET', 'POST'])
def consultar_cita():
    if request.method == 'GET':
        return render_template('citas/consultar_cita.html')
    if request.method == 'POST':
        id = request.form['Identificación']
        paciente = hospital.buscar_paciente(id)
        if paciente:
            session['identificacion'] = id
            return redirect(url_for('main.agendar_cita'))
            
        else: 
            return render_template('citas/consultar_cita.html', error="Esa identificación no existe.")        

    
@main.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if request.method == 'POST':
        #identificacion = request.args.get('identi')
        identifica = session.get('identificacion')
        paciente = hospital.buscar_paciente(identifica)
        medico_nombre = request.form['medicos']
        medico = hospital.buscar_medico_nombre(medico_nombre)
        fecha_hora = datetime.strptime(f"{request.form['fecha']} {request.form['hora']}", '%Y-%m-%d %H:%M')
        urgente = request.form['urgente']

        cita = Cita(paciente, medico, fecha_hora, urgente)
        hospital.agenda.agendar_cita(cita)
        #print(cita)
        return redirect(url_for('main.agendar_cita'))

    if request.method == 'GET':
        identifica = session.get('identificacion')
        especialidades = list(set(medico.especialidad for medico in hospital.medicos))
        nombre = hospital.buscar_paciente(identifica).nombre

        return render_template('citas/agendar_cita.html', nombre=nombre,identifica=identifica,especialidades=especialidades)


@main.route('/cancelar_cita', methods=['GET', 'POST'])
def cancelar_cita():
    if request.method == 'GET':
        identificacion = session.get('identificacion')
        nombre = hospital.buscar_paciente(identificacion).nombre
        paciente_id = hospital.buscar_paciente(identificacion)

        citas = hospital.agenda.buscar_citas_paciente(paciente_id)
            
        return render_template('citas/cancelar_cita.html',identificacion=identificacion,nombre=nombre,citas=citas)

    if request.method == 'POST':
        identificacion = session.get('identificacion')
        paciente = hospital.buscar_paciente(identificacion)
        citas = hospital.agenda.buscar_citas_paciente(paciente)
        cita = request.form['citas']
        paciente_cita = None
        for c in citas:
            if (c.medico.nombre and c.fecha_hora.strftime('%Y-%m-%d %H:%M')) in cita:
                paciente_cita = c
        print(paciente_cita)
        hospital.agenda.cancelar_cita(paciente_cita)
        return redirect(url_for('main.cancelar_cita'))

@main.route('/mover_cita', methods=['GET', 'POST'])
def mover_cita():
    if request.method == 'GET':
        identificacion = session.get('identificacion')
        nombre = hospital.buscar_paciente(identificacion).nombre
        paciente_id = hospital.buscar_paciente(identificacion)

        citas = hospital.agenda.buscar_citas_paciente(paciente_id)
            
        return render_template('citas/mover_cita.html',identificacion=identificacion,nombre=nombre,citas=citas)
    
    if request.method == 'POST':
        identificacion = session.get('identificacion')
        paciente = hospital.buscar_paciente(identificacion)
        citas = hospital.agenda.buscar_citas_paciente(paciente)
        cita = request.form['citas']
        fecha_n = request.form['fecha']
        hora_n = request.form['hora']
        urgente = request.form['urgente']
        fecha_hora_n = datetime.strptime(f"{fecha_n} {hora_n}", "%Y-%m-%d %H:%M")
        paciente_cita = None
        for c in citas:
            if (c.medico.nombre and c.fecha_hora.strftime('%Y-%m-%d %H:%M')) in cita:
                paciente_cita = c
        
        hospital.agenda.mover_cita(paciente_cita, fecha_hora_n, urgente)
        return redirect(url_for('main.mover_cita'))


# Rutas para Paciente: Agregar Paciente, Actualizar Paciente, Borrar Paciente, Lista de Pacientes
@main.route('/agregar_paciente', methods=['GET', 'POST'])
def agregar_paciente():
    if request.method == 'GET':
        return render_template('pacientes/agregar_paciente.html')
    
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        celular = request.form['celular']
        email = request.form['email']
        paciente = Paciente(id, nombre, celular, email)
        hospital.agregar_paciente(paciente)
        print(paciente)
        return redirect(url_for('main.agregar_paciente'))
    

@main.route('/consultar_paciente', methods=['GET', 'POST'])
def consultar_paciente():
    if request.method == 'GET':
        return render_template('pacientes/consultar_paciente.html')
    
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'actualizar':
            id = request.form['consulta']
            nombre = request.form['nombre']
            celular = request.form['celular']
            email = request.form['email']

            paciente = hospital.buscar_paciente(id)
            paciente.nombre = nombre
            paciente.celular = celular
            paciente.correo = email
        if accion == 'borrar':
            id = request.form['consulta']
            paciente = hospital.buscar_paciente(id)
            hospital.borrar_paciente(paciente)

        return redirect(url_for('main.consultar_paciente'))


@main.route('/lista_paciente')
def lista_paciente():
    datos = hospital.pacientes
    return render_template('pacientes/lista_paciente.html', datos=datos)    


# Rutas para Medico: Agregar Medico, Actualizar Medico, Borrar Medico y Lista de Medicos

@main.route('/agregar_medico', methods=['GET', 'POST'])
def agregar_medico():
    if request.method == 'GET':
        return render_template('medicos/agregar_medico.html')
    
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        celular = request.form['celular']
        especialidad = request.form['especialidad']
        medico = Medico(id, nombre, celular, especialidad)
        hospital.agregar_medico(medico)
        print(medico)
        return redirect(url_for('main.agregar_medico'))
    

@main.route('/consultar_medico', methods=['GET', 'POST'])
def consultar_medico():
    if request.method == 'GET':
        return render_template('medicos/consultar_medico.html')
    
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'actualizar':
            id = request.form['consulta']
            nombre = request.form['nombre']
            celular = request.form['celular']
            especialidad = request.form['especialidad']

            Medico = hospital.buscar_medico(id)
            Medico.nombre = nombre
            Medico.celular = celular
            Medico.especialidad = especialidad
        if accion == 'borrar':
            id = request.form['consulta']
            Medico = hospital.buscar_medico(id)
            hospital.borrar_medico(Medico)

        return redirect(url_for('main.consultar_medico'))


@main.route('/lista_medico')
def lista_medico():
    datos = hospital.medicos
    return render_template('medicos/lista_medico.html', datos=datos)


# Rutas para la solicitudes en javascript y el intercambio de datos para las validaciones en cita, paciente y medico 

@main.route('/proceso', methods=['POST'])  # Ruta para actualizar la lista de medicos segun la especialidad seleccionada
def proceso():                             # Se maneja con javascript para que se actualice en tiempo real 
    especialida = request.form['especialida']
    opciones = hospital.buscar_medicos_por_especialidad(especialida)
    return jsonify(opciones)


@main.route('/proceso_agendar_cita')           # Se utiliza para verificar la fecha y hora y de esa manera
def proceso_agendar_cita():                    # se manda a javascript para que lanze las excepciones en que caso de 
    medico_nombre = request.args.get('medico') # que la fecha ya este ocupada
    fecha_hora = datetime.strptime(request.args.get('fecha_hora'), '%Y-%m-%d %H:%M') 
    medico = hospital.buscar_medico_nombre(medico_nombre) 
    citas = hospital.agenda.citas
    print(medico_nombre) 
    for cita in citas: 
        if cita.medico == medico and cita.fecha_hora == fecha_hora: 
            return jsonify({'exists': True}) 
        
    return jsonify({'exists': False})

@main.route('/proceso_mover_cita')
def proceso_mover_cita():
    medico_nombre = request.args.get('medico') # Igual que agendar pero con el de mover cita
    fecha_hora = datetime.strptime(request.args.get('fecha_hora'), '%Y-%m-%d %H:%M') 
    medico = hospital.buscar_medico_nombre(medico_nombre) 
    citas = hospital.agenda.citas 
    print(medico_nombre)
    for cita in citas: 
        if cita.medico == medico and cita.fecha_hora == fecha_hora: 
            return jsonify({'exists': True}) 
        
    return jsonify({'exists': False})

@main.route('/proceso_actualizar')  # Se utiliza para llenar los campos del paciente con el id dado
def proceso_actualizar():           # mandando los datos por medio de javascript para que se actualice 
    id = request.args.get('id')     # una vez se ingrese el id y se presione el boton buscar
    paciente = hospital.buscar_paciente(id)
    if paciente:
        return jsonify(paciente.dicc())
    else:
        print(id)
        return jsonify({"error": "Paciente no encontrado"}), 404    

@main.route('/proceso_medico')  # Igual al de paciente pero con el medico
def proceso_medico():                         
    id = request.args.get('id')
    medico = hospital.buscar_medico(id)
    if medico:
        return jsonify(medico.dicc())
    else:
        print(id)
        return jsonify({"error": "Medico no encontrado"}), 404 
    

@main.route('/verificar_paciente') # Para verificar que el paciente ya existe
def verificar_paciente():
    paciente_id = request.args.get('id')
    paciente = hospital.buscar_paciente(paciente_id)
    
    if paciente:
        return jsonify({'exists': True})
            
    else:
        return jsonify({'exists': False})
            
    

@main.route('/verificar_medico') # Verificar que el medico ya existe
def verificar_medico():
    medico_id = request.args.get('id')
    medico = hospital.buscar_medico(medico_id)

    if medico:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})    
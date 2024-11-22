# Proyecto de Gestión de Citas Médicas con Flask

Este es un proyecto web desarrollado con Flask para la gestión de citas médicas. Permite registrar pacientes, programar citas, Ver listado de pacientes, ver listados de citas y tambien se puede elminar o cancelar cita. Permite registrar medicos, eliminar, consultar listados de los medicos y consultar la lista de los medicos.

## Características:

- Registro de pacientes,
- Registo de Medicos,
- Registo de citas,
- Ver lista de pacientes,
- Ver Lista de Medicos.
- Eliminar pacientes, Eliminar medicos, cancelar y mover citas,
- consultar cita que tiene el medicos en el dia.

## listado de pacientes y medicos                        
- Lista citas en un archivo CSV                  
- Lista Pacientes en un archivo CSV               
- Lista medicos en un archivo Json

## Tecnologías Utilizadas:

- *Python* : Lenguaje utilizado
- *Flask* : Framework web utilizado.   
- *HTML y CSS*: Para la implementacion y el diseño de la interfaz de usuario.   
- *Jscript*: Para el manejo de los datos y que se vea en tiempo de ejecucion.
- *Jinja*: Para manejo datos de Flask y HTML

## Requisitos Previos

- Python instalado en el sistema.                    
- Visual Code para crear entornos virtuales (Python).           
- Instalación de las dependencias necesarias.

## Ejecucion
Comando para ejecutar el proyecto
```bash
cd Citas Medicas
python main.py
```

## Issues Corregidos

- Se implementó una interfaz web con Flask en lugar de hacerlo en consola con Rich
- Se arregló el super menu simplificandolo en 3 opciones:
    - Inicio, Citas, Paciente, Medico
- Se acomodó el apartado citas urgentes para que dentro citas se pudiera agregar directamente
- Se acomodó la fecha para que al momento de agendar no hiciera conflicto con una ya registrada
- tanto en el apartado paciente como medico se puede visualizar las lista de los pacientes y medicos registrados
- Se manejó el apartado agregar_paciente y agregar_medico para que no registraran identificaciones ya existentes    

## Autores:

- Creado por [Nicolas Martinez](https://github.com/NicolasMFDev)
- Creado por [Carlos Ruiz](https://github.com/HernanWow)
- Creado por [Julian ](https://github.com/B4ST1D4S2426)

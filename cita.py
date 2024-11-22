class Cita:
    def __init__(self, paciente, medico, fecha_hora,urgente):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.urgente = urgente

        self.motivo_cancelacion = None
        self.calificacion = None
        self.comentario = None

    def __repr__(self):
        return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"


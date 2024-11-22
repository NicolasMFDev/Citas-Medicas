from rich.console import Console

console = Console()


class Agenda:
    def __init__(self):
        self.citas = []

    def agendar_cita(self, cita):
        # Verificar si hay conflicto de horarios
        for c in self.citas:
            if c.medico == cita.medico and c.fecha_hora == cita.fecha_hora:
                if cita.urgente and not c.urgente:
                    nueva_fecha = self.encontrar_siguiente_horario_disponible(c.medico, c.fecha_hora)
                    c.fecha_hora = nueva_fecha
                    break
                else:
                    raise ValueError(
                        "Ya existe una cita en ese horario para este médico."
                    )

        self.citas.append(cita)

    def encontrar_siguiente_horario_disponible(self, medico, fecha_hora):
        # Lógica simple: buscar el siguiente horario disponible en intervalos de 1 hora
        nueva_fecha = fecha_hora
        while True:
            nueva_fecha = nueva_fecha.replace(hour=(nueva_fecha.hour + 1) % 24)
            if not any(
                c.medico == medico and c.fecha_hora == nueva_fecha for c in self.citas
            ):
                return nueva_fecha

    def cancelar_cita(self, cita):
        if cita in self.citas:
            self.citas.remove(cita)
            #cita.motivo_cancelacion = motivo
        else:
            print("No se pudo")    
        

    def mover_cita(self, cita, nueva_fecha_hora, cita_urgente):
        if cita in self.citas:
            cita.fecha_hora = nueva_fecha_hora
            cita.urgente = cita_urgente


    def buscar_citas_paciente(self, paciente):
        return [cita for cita in self.citas if cita.paciente == paciente]

    def buscar_citas_medico(self, medico):
        return [cita for cita in self.citas if cita.medico == medico]
    

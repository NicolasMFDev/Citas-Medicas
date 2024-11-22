from persona import Persona


class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular)
        self.correo = correo


    def dicc(self):
        return {
            'id': self.identificacion,
            'nombre': self.nombre,
            'celular': self.celular,
            'email': self.correo
        }    

    def __str__(self):
        return f'Paciente(identificacion={self.identificacion}, nombre={self.nombre}, celular={self.celular}, correo={self.correo})'
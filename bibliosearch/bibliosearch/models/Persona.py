class Persona(object):

    #Constructor de Persona
    def __init__(self,id_persona, nombre, apellidos):
        self._id = id_persona
        self._nombre = nombre
        self._apellidos = apellidos

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_apellidos(self):
        return self._apellidos
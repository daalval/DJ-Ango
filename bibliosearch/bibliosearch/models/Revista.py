class Revista(object):
    #Constructor de Revista
    def __init__(self, id_revista, nombre):
        self._id = id_revista
        self._nombre = nombre

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre
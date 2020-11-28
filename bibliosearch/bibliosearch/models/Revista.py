class Revista(object):
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre
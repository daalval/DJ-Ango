class Revista(object):
    def __init__(self, nombre):
        self._nombre = nombre

    def get_nombre(self):
        return self._nombre
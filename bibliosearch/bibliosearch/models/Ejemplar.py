class Ejemplar(object):
    def __init__(self, id, volumen, numero, mes, revista):
        self._id = id
        self._volumen = volumen
        self._numero = numero
        self._mes = mes
        self._revista = revista
        
    def get_id(self):
        return self._id

    def get_volumen(self):
        return self._volumen

    def get_numero(self):
        return self._numero

    def get_mes(self):
        return self._mes

    def get_revista(self):
        return self._revista

        
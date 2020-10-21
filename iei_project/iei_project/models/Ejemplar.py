class Ejemplar(object):
    def __init__(self, volumen, numero, mes):
        self._volumen = volumen
        self._numero = numero
        self._mes = mes
    
    def get_volumen(self):
        return self._volumen

    def get_numero(self):
        return self._numero

    def get_mes(self):
        return self._mes
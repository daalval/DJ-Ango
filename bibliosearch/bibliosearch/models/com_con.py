from bibliosearch.models.Publicacion import Publicacion

class Com_con(Publicacion):
    """
    Clase comunicaciones-congresos
    """
    def __init__(self, congreso, edicion, lugar, pagina_inicio, pagina_fin, id_publicacion, titulo, anyo, url, autores):
        self._congreso = congreso
        self._edicion = edicion
        self._lugar = lugar
        self._pagina_inicio = pagina_inicio
        self._pagina_fin = pagina_fin
        super().__init__(id_publicacion, titulo, anyo, url, autores)

    def get_congreso(self):
        return(self._congreso)
    
    def get_edicion(self):
        return(self._edicion)

    def get_lugar(self):
        return(self._lugar)

    def get_pagina_inicio(self):
        return(self._pagina_inicio)
    
    def get_pagina_fin(self):
        return(self._pagina_fin)

    def get_type(self):
        return self.__class__.__name__

def dict_2_com_con(dict):
    return Com_con(dict['congreso'],dict['edicion'],dict['lugar'],dict['pagina_inicio'],dict['pagina_fin'],None,dict['titulo'],dict['anyo'],dict['URL'],dict['autores'])
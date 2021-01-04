from bibliosearch.models.Publicacion import Publicacion

class Articulo(Publicacion):
    """
    Clase artículo
    """
    def __init__(self, pagina_inicio, pagina_fin, id_publicacion, titulo, anyo, url, autores, ejemplar):
        self._pagina_inicio = pagina_inicio
        self._pagina_fin = pagina_fin
        self._ejemplar = ejemplar
        super().__init__(id_publicacion, titulo, anyo, url, autores)
    
    def get_pagina_inicio(self):
        return(self._pagina_inicio)
    
    def get_pagina_fin(self):
        return(self._pagina_fin)

    def get_ejemplar(self):
        return(self._ejemplar)

def dict_2_articulo(dict):
    return Articulo(dict['pagina_inicio'],dict['pagina_fin'],None,dict['titulo'],dict['anyo'],dict['URL'],dict['autores'],dict['nombre'])
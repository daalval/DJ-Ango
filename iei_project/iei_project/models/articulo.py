from iei_project.models.publicacion import Publicacion

class Articulo(Publicacion):
    """
    Clase artículo
    """
    def __init__(self, pagina_inicio, pagina_fin, titulo, anyo, url, autores):
        self._pagina_inicio = pagina_inicio
        self._pagina_fin = pagina_fin
        super().__init__(titulo, anyo, url, autores)
    
    def get_pagina_incio(self):
        return(self._pagina_inicio)
    
    def get_pagina_fin(self):
        return(self._pagina_fin)
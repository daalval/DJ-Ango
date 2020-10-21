class Articulo:
    """
    Clase artículo
    """
    def __init__(self, pagina_inicio, pagina_fin):
        self._pagina_inicio = pagina_inicio
        self._pagina_fin = pagina_fin
    
    def get_pagina_incio(self):
        return(self._pagina_inicio)
    
    def get_pagina_fin(self):
        return(self._pagina_fin)
class Com_con:
    """
    Clase comunicaciones-congresos
    """
    def __init__(self, congreso, edicion, lugar, pagina_inicio, pagina_fin):
        self._congreso = congreso
        self._edicion = edicion
        self._lugar = lugar
        self._pagina_inicio = pagina_inicio
        self._pagina_fin = pagina_fin

    def get_congreso(self):
        return(self._congreso)
    
    def get_edicion(self):
        return(self._edicion)

    def get_lugar(self):
        return(self._lugar)

    def get_pagina_incio(self):
        return(self._pagina_inicio)
    
    def get_pagina_fin(self):
        return(self._pagina_fin)

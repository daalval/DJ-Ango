class Publicacion(object):

    #Constructor de Publicacion
    def __init__(self, id_publicacion, titulo, anyo, url, autores):
        self._id = id_publicacion
        self._titulo = titulo
        self._anyo = anyo
        self._url = url
        self._autores = autores

    def get_id(self):
        return(self._id)

    def get_titulo(self):
        return(self._titulo)

    def get_anyo(self):
        return(self._anyo)
    
    def get_url(self):
        return(self._url)

    def get_autores(self):
        return(self._autores)
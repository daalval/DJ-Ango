class Publicacion(object):

    def __init__(self, id, titulo, anyo, url, autores):
        self._id = id
        self._titulo = titulo
        self._anyo = anyo
        self._url = url
        self._autores = autores


    def get_id(self):
        return(self.id)

    def get_titulo(self):
        return(self._titulo)

    def get_anyo(self):
        return(self._anyo)
    
    def get_url(self):
        return(self._url)

    def get_autores(self):
        return(self._autores)
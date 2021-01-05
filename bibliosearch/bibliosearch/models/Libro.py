from bibliosearch.models.Publicacion import Publicacion

LIBRO = 'libro'

class Libro(Publicacion):

    def __init__(self, editorial, id_publicacion, titulo, anyo, url, autores):
        self._editorial = editorial
        super().__init__(id_publicacion, titulo, anyo, url, autores)

    def get_editorial(self):
        return self._editorial
    
    def get_type(self):
        return self.__class__.__name__

def dict_2_libro(dict):
    return Libro(dict['editorial'],None,dict['titulo'],dict['anyo'],dict['URL'],dict['autores'])

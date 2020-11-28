from bibliosearch.models.Publicacion import Publicacion


class Libro(Publicacion):

    def __init__(self, editorial, id_publicacion, titulo, anyo, url, autores):
        self._editorial = editorial
        super().__init__(id_publicacion, titulo, anyo, url, autores)

    def get_editorial(self):
        return self._editorial
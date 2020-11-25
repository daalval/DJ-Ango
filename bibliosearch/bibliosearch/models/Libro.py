from bibliosearch.models.Publicacion import Publicacion


class Libro(Publicacion):

    def __init__(self, editorial, paginas,titulo, anyo, url, autores):
        self._editorial = editorial
        self._paginas = paginas
        super().__init__(titulo, anyo, url, autores)

    def get_editorial(self):
        return self._editorial

    def get_paginas(self):
        return self._paginas
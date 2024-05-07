def obtener_informacion(self):
        #Devuelve una cadena con la información detallada de la película.
        info = (
            f"Titulo: {self.titulo}\n"
            f"Genero: {self.genero}\n"
            f"Año de lanzamiento: {self.anio_lanzamiento}\n"
            f"Duracion: {self.duracion} minutos\n"
            f"Director: {self.director}\n"
            f"Actores: {', '.join(self.actores)}\n"
            f"Calificacion: {self.calificacion}/10\n"
            f"Sinopsis: {self.sinopsis}"
        )
        return info
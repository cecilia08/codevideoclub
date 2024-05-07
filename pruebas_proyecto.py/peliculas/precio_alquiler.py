def precio_alquiler(self):
        # Método para calcular el precio de alquiler de la película.
        # El precio podría depender del año de lanzamiento o de la popularidad.
        return 5.90 if self.anio_lanzamiento > 2010 else 2.99
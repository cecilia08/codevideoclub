def __init__(self, titulo, genero, anio_lanzamiento, duracion, director, actores, calificacion, sinopsis):
        # Constructor de la clase Pelicula que inicializa los atributos de la película.
        self.titulo = titulo
        self.genero = genero
        self.anio_lanzamiento = anio_lanzamiento
        self.duracion = duracion
        self.director = director
        self.actores = actores  # lista de nombres de actores.
        self.calificacion = calificacion
        self.sinopsis = sinopsis
        self.stock = 10  #  stock inicial  para la película.
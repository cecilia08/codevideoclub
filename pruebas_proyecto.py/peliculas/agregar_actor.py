def agregar_actor(self, actor):
        #Método para agregar un actor a la lista de actores de la película.
        if actor not in self.actores:
            self.actores.append(actor)
def recomendacion_clientes(self):
        # Método que devuelve una recomendación para los clientes sobre la película, según su calificación.
        if self.calificacion >= 8:
            return "Altamente recomendada!"
        elif self.calificacion >= 5:
            return "Tiene sus momentos."
        else:
            return "Podría ser mejor. Considera otras opciones."

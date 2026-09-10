class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

    def __str__(self):
        return str(self.valor)


class DNodo:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.proximo = None

    def __str__(self):
        return str(self.valor)

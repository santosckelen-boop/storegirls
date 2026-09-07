class Fila:
    def __init__(self):
        self._lista_de_valores = []

    def enqueue(self, item):
        if item is None:
            raise ValueError("Valores nulos nao podem ser adicionados a fila.")

        self._lista_de_valores.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Nao ha dados para remover da fila.")

        return self._lista_de_valores.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("Nao ha dados na fila.")

        return self._lista_de_valores[0]

    def remover_ultima(self):
        if self.is_empty():
            raise IndexError("Nao ha dados na fila.")

        return self._lista_de_valores.pop()

    def is_empty(self):
        return len(self._lista_de_valores) == 0

    def size(self):
        return len(self._lista_de_valores)

    def listar(self):
        return list(self._lista_de_valores)

    def __len__(self):
        return len(self._lista_de_valores)

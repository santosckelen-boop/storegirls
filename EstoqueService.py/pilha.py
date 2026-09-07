class Pilha:
    def __init__(self):
        self._lista_de_valores = []

    def push(self, valor):
        if valor is None:
            raise ValueError("Valores nulos nao podem ser adicionados a pilha.")

        self._lista_de_valores.insert(0, valor)

    def pop(self):
        if self.is_empty():
            raise IndexError("A pilha esta vazia.")

        return self._lista_de_valores.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("A pilha esta vazia.")

        return self._lista_de_valores[0]

    def is_empty(self):
        return len(self._lista_de_valores) == 0

    def __len__(self):
        return len(self._lista_de_valores)
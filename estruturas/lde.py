from estruturas.nodo import DNodo

class LDE:
    def __init__(self):
        self.header = DNodo(None)
        self.trailer = DNodo(None)
        self.header.proximo = self.trailer
        self.trailer.anterior = self.header
        self.quantidade_itens = 0

    def is_empty(self):
        return (
            self.header.proximo == self.trailer
            and self.trailer.anterior == self.header
            and self.quantidade_itens == 0
        )

    def inserir_inicio(self, valor):
        if valor is None:
            raise ValueError("Valores nulos nao podem ser adicionados.")

        novo_nodo = DNodo(valor)
        primeiro = self.header.proximo

        self.header.proximo = novo_nodo
        novo_nodo.anterior = self.header
        novo_nodo.proximo = primeiro
        primeiro.anterior = novo_nodo
        self.quantidade_itens += 1

    def inserir_fim(self, valor):
        if valor is None:
            raise ValueError("Valores nulos nao podem ser adicionados.")

        novo_nodo = DNodo(valor)
        ultimo = self.trailer.anterior

        ultimo.proximo = novo_nodo
        novo_nodo.anterior = ultimo
        novo_nodo.proximo = self.trailer
        self.trailer.anterior = novo_nodo

        self.quantidade_itens += 1

    def inserir_posicao(self, posicao, valor):
        if valor is None:
            raise ValueError("Valores nulos nao podem ser adicionados.")

        if posicao < 0 or posicao > self.quantidade_itens:
            raise IndexError("Posicao invalida na lista.")

        if posicao == self.quantidade_itens:
            self.inserir_fim(valor)
            return

        proximo_nodo = self.header.proximo

        for _ in range(posicao):
            proximo_nodo = proximo_nodo.proximo

        novo_nodo = DNodo(valor)
        anterior = proximo_nodo.anterior

        anterior.proximo = novo_nodo
        novo_nodo.anterior = anterior
        novo_nodo.proximo = proximo_nodo
        proximo_nodo.anterior = novo_nodo
        self.quantidade_itens += 1

    def buscar(self, codigo):
        atual = self.header.proximo

        while atual != self.trailer:
            if atual.valor.get_identificador_unico() == codigo:
                return atual.valor

            atual = atual.proximo

        return None

    def remover(self, codigo):
        atual = self.header.proximo

        while atual != self.trailer:
            if atual.valor.get_identificador_unico() == codigo:
                atual.anterior.proximo = atual.proximo
                atual.proximo.anterior = atual.anterior

                atual.anterior = None
                atual.proximo = None
                self.quantidade_itens -= 1
                return atual.valor

            atual = atual.proximo

        return None

    def remover_inicio(self):
        if self.is_empty():
            return None

        removido = self.header.proximo
        novo_primeiro = removido.proximo

        self.header.proximo = novo_primeiro
        novo_primeiro.anterior = self.header
        removido.anterior = None
        removido.proximo = None
        self.quantidade_itens -= 1
        return removido.valor

    def remover_fim(self):
        if self.is_empty():
            return None

        removido = self.trailer.anterior
        novo_ultimo = removido.anterior

        novo_ultimo.proximo = self.trailer
        self.trailer.anterior = novo_ultimo
        removido.anterior = None
        removido.proximo = None
        self.quantidade_itens -= 1
        return removido.valor

    def listar(self):
        valores = []
        atual = self.header.proximo

        while atual != self.trailer:
            valores.append(atual.valor)
            atual = atual.proximo

        return valores

    def listar_inverso(self):
        valores = []
        atual = self.trailer.anterior

        while atual != self.header:
            valores.append(atual.valor)
            atual = atual.anterior

        return valores

    def __len__(self):
        return self.quantidade_itens
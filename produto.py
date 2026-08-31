import math


class Produto:
    def __init__(self, codigo, nome, preco, quantidade):
        if isinstance(codigo, bool):
            raise ValueError("O ID do produto deve ser um numero inteiro.")

        try:
            self.codigo = int(codigo)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("O ID do produto deve ser um numero inteiro.")

        if isinstance(codigo, float) and not codigo.is_integer():
            raise ValueError("O ID do produto deve ser um numero inteiro.")

        if not isinstance(nome, str):
            raise ValueError("O nome do produto e obrigatorio.")

        self.nome = nome.strip()

        if isinstance(preco, bool):
            raise ValueError("O preco do produto deve ser um numero.")

        try:
            self.preco = float(preco)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("O preco do produto deve ser um numero.")

        if isinstance(quantidade, bool):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        try:
            self.quantidade = int(quantidade)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if isinstance(quantidade, float) and not quantidade.is_integer():
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if self.codigo <= 0:
            raise ValueError("O ID do produto deve ser maior que zero.")

        if self.nome == "":
            raise ValueError("O nome do produto e obrigatorio.")

        if not math.isfinite(self.preco) or self.preco <= 0:
            raise ValueError("O preco do produto deve ser maior que zero.")

        if self.quantidade < 0:
            raise ValueError("A quantidade nao pode ser negativa.")

    def get_identificador_unico(self):
        return self.codigo

    def atualizar_estoque(self, nova_quantidade):
        if isinstance(nova_quantidade, bool):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        try:
            quantidade = int(nova_quantidade)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if isinstance(nova_quantidade, float) and not nova_quantidade.is_integer():
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if quantidade < 0:
            raise ValueError("A quantidade nao pode ser negativa.")

        self.quantidade = quantidade

    def to_csv_row(self):
        return [self.codigo, self.nome, self.preco, self.quantidade]

    def __str__(self):
        preco_formatado = f"{self.preco:.2f}"
        return f"Produto {self.codigo} - {self.nome} | R$ {preco_formatado} | Estoque: {self.quantidade}"

def produto_from_csv_row(row):
    return Produto(row["codigo"], row["nome"], row["preco"], row["quantidade"])

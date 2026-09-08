import math


class Venda:
    def __init__(self, codigo, codigo_cliente, itens, valor_total=None):
        if isinstance(codigo, bool) or isinstance(codigo_cliente, bool):
            raise ValueError("Os IDs da venda devem ser numeros inteiros.")

        try:
            self.codigo = int(codigo)
            self.codigo_cliente = int(codigo_cliente)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("Os IDs da venda devem ser numeros inteiros.")

        if isinstance(codigo, float) and not codigo.is_integer():
            raise ValueError("O ID da venda deve ser um numero inteiro.")

        if isinstance(codigo_cliente, float) and not codigo_cliente.is_integer():
            raise ValueError("O ID do cliente deve ser um numero inteiro.")
        if not isinstance(itens, list):
            raise ValueError("Os itens da venda devem ser informados em uma lista.")

        self.itens = []

        if self.codigo <= 0:
            raise ValueError("O ID da venda deve ser maior que zero.")

        if self.codigo_cliente <= 0:
            raise ValueError("O ID do cliente deve ser maior que zero.")

        if len(itens) == 0:
            raise ValueError("A venda deve possuir pelo menos um item.")

        for item in itens:
            if not isinstance(item, dict):
                raise ValueError("Item de venda invalido.")

            try:
                codigo_original = item["codigo_produto"]
                quantidade_original = item["quantidade"]
                preco_original = item["preco_unitario"]

                if isinstance(codigo_original, bool) or isinstance(
                    quantidade_original, bool
                ) or isinstance(preco_original, bool):
                    raise ValueError

                codigo_produto = int(codigo_original)
                quantidade = int(quantidade_original)
                preco_unitario = float(preco_original)
            except (KeyError, OverflowError, TypeError, ValueError):
                raise ValueError("Item de venda invalido.")

            if isinstance(codigo_original, float) and not codigo_original.is_integer():
                raise ValueError("O ID do produto deve ser um numero inteiro.")

            if isinstance(quantidade_original, float) and not quantidade_original.is_integer():
                raise ValueError("A quantidade vendida deve ser um numero inteiro.")

            if codigo_produto <= 0:
                raise ValueError("O ID do produto deve ser maior que zero.")

            if quantidade <= 0:
                raise ValueError("A quantidade vendida deve ser maior que zero.")

            if not math.isfinite(preco_unitario) or preco_unitario <= 0:
                raise ValueError("O preco unitario deve ser maior que zero.")

            self.itens.append(
                {
                    "codigo_produto": codigo_produto,
                    "quantidade": quantidade,
                    "preco_unitario": preco_unitario,
                }
            )

        total_calculado = self.calcular_total()

        if valor_total is not None:
            if isinstance(valor_total, bool):
                raise ValueError("O valor total da venda e invalido.")

            try:
                total_salvo = float(valor_total)
            except (OverflowError, TypeError, ValueError):
                raise ValueError("O valor total da venda e invalido.")

            if not math.isfinite(total_salvo) or abs(total_salvo - total_calculado) > 0.01:
                raise ValueError("O valor total da venda nao corresponde aos itens.")

        self.valor_total = total_calculado

    def calcular_total(self):
        total = 0.0

        for item in self.itens:
            total += item["quantidade"] * item["preco_unitario"]

        return round(total, 2)

    def itens_para_texto(self):
        partes = []
        for item in self.itens:
            partes.append(
                f"{item['codigo_produto']}:{item['quantidade']}:{item['preco_unitario']}"
            )
        return "|".join(partes)

    def to_csv_row(self):
        return [self.codigo, self.codigo_cliente, self.itens_para_texto(), self.valor_total]

    def __str__(self):
        valor_formatado = f"{self.valor_total:.2f}"
        itens_formatados = []

        for item in self.itens:
            preco = f"{item['preco_unitario']:.2f}"
            itens_formatados.append(
                f"Produto {item['codigo_produto']}: "
                f"{item['quantidade']} un. x R$ {preco}"
            )

        texto_itens = "; ".join(itens_formatados)
        return (
            f"Venda {self.codigo} | Cliente {self.codigo_cliente} | "
            f"Itens: {texto_itens} | Total R$ {valor_formatado}"
        )

def itens_de_texto(texto):
    itens = []

    if not isinstance(texto, str):
        raise ValueError("O campo de itens da venda e invalido.")

    if texto.strip() == "":
        return itens

    for parte in texto.split("|"):
        codigo_produto, quantidade, preco_unitario = parte.split(":")
        itens.append(
            {
                "codigo_produto": int(codigo_produto),
                "quantidade": int(quantidade),
                "preco_unitario": float(preco_unitario),
            }
        )

    return itens

def venda_from_csv_row(row):
    return Venda(
        row["codigo"],
        row["codigo_cliente"],
        itens_de_texto(row["itens"]),
        row["valor_total"],
    )

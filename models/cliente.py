class Cliente:
    def __init__(self, codigo, nome):
        if isinstance(codigo, bool):
            raise ValueError("O ID do cliente deve ser um numero inteiro.")

        try:
            self.codigo = int(codigo)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("O ID do cliente deve ser um numero inteiro.")

        if isinstance(codigo, float) and not codigo.is_integer():
            raise ValueError("O ID do cliente deve ser um numero inteiro.")

        if not isinstance(nome, str):
            raise ValueError("O nome do cliente e obrigatorio.")

        self.nome = nome.strip()

        if self.codigo <= 0:
            raise ValueError("O ID do cliente deve ser maior que zero.")

        if self.nome == "":
            raise ValueError("O nome do cliente e obrigatorio.")

    def get_identificador_unico(self):
        return self.codigo

    def to_csv_row(self):
        return [self.codigo, self.nome]

    def __str__(self):
        return f"Cliente {self.codigo} - {self.nome}"

def cliente_from_csv_row(row):
    return Cliente(row["codigo"], row["nome"])

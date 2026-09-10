def cadastrar_cliente(self, nome):
    cliente = Cliente(self.gerar_proximo_codigo_cliente(), nome)
    posicao = len(self.clientes)
    self.clientes.inserir_fim(cliente)

    try:
        self.salvar_clientes()
    except OSError:
        self.clientes.remover(cliente.codigo)
        raise

    self.historico.push(
        {"tipo": "cadastro_cliente", "cliente": cliente, "posicao": posicao}
        )
    return cliente

def listar_clientes(self):
    return self.clientes.listar()

def buscar_cliente(self, codigo):
    codigo = self._validar_codigo(codigo, "ID do cliente")
    return self.clientes.buscar(codigo)

def remover_cliente(self, codigo):
    codigo = self._validar_codigo(codigo, "ID do cliente")

    for venda in self.vendas.listar():
        if venda.codigo_cliente == codigo:
            raise ValueError(
                "O cliente nao pode ser removido porque possui vendas registradas."
            )

    posicao = self._buscar_posicao(self.clientes.listar(), codigo)

    if posicao == -1:
        raise ValueError("Cliente nao encontrado.")

    cliente = self.clientes.remover(codigo)

    try:
        self.salvar_clientes()
    except OSError:
        self.clientes.inserir_posicao(posicao, cliente)
        raise

    self.historico.push(
        {"tipo": "remocao_cliente", "cliente": cliente, "posicao": posicao}
    )
    return cliente

def cadastrar_produto(self, nome, preco, quantidade):
    produto = Produto(
        self.gerar_proximo_codigo_produto(),
        nome,
        preco,
        quantidade,
    )
    posicao = len(self.produtos)
    self.produtos.inserir_fim(produto)

    try:
        self.salvar_produtos()
    except OSError:
        self.produtos.remover(produto.codigo)
        raise

    self.historico.push(
        {"tipo": "cadastro_produto", "produto": produto, "posicao": posicao}
    )
    return produto

def listar_produtos(self):
    return self.produtos.listar()

def listar_produtos_inverso(self):
    return self.produtos.listar_inverso()

def listar_produtos_ordenados_por_id(self):
    produtos = self.produtos.listar()
    return ordenar_produtos_por_id(produtos)

def buscar_produto(self, codigo):
    codigo = self._validar_codigo(codigo, "ID do produto")
    return self.produtos.buscar(codigo)

def buscar_produto_binario(self, codigo):
    codigo = self._validar_codigo(codigo, "ID do produto")
    produtos_ordenados = self.listar_produtos_ordenados_por_id()
    return buscar_produto_por_id(produtos_ordenados, codigo)

def atualizar_estoque(self, codigo, nova_quantidade):
    codigo = self._validar_codigo(codigo, "ID do produto")
    nova_quantidade = self._validar_quantidade(nova_quantidade, permite_zero=True)
    produto = self.produtos.buscar(codigo)

    if produto is None:
        raise ValueError("Produto nao encontrado.")

    quantidade_anterior = produto.quantidade
    produto.atualizar_estoque(nova_quantidade)

    try:
        self.salvar_produtos()
    except OSError:
        produto.atualizar_estoque(quantidade_anterior)
        raise

    self.historico.push(
        {
            "tipo": "atualizacao_estoque",
            "produto": produto,
            "quantidade_anterior": quantidade_anterior,
            "quantidade_nova": nova_quantidade,
        }
    )
    return produto

def remover_produto(self, codigo):
    codigo = self._validar_codigo(codigo, "ID do produto")

    for venda in self.vendas.listar():
        for item in venda.itens:
            if item["codigo_produto"] == codigo:
                raise ValueError(
                    "O produto nao pode ser removido porque possui vendas registradas."
                )

    posicao = self._buscar_posicao(self.produtos.listar(), codigo)

    if posicao == -1:
        raise ValueError("Produto nao encontrado.")

    produto = self.produtos.remover(codigo)

    try:
        self.salvar_produtos()
    except OSError:
        self.produtos.inserir_posicao(posicao, produto)
        raise

    self.historico.push(
        {"tipo": "remocao_produto", "produto": produto, "posicao": posicao}
    )
    return produto

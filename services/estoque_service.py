import os
from contextlib import suppress

from algoritmos.busca_binaria import buscar_produto_por_id
from algoritmos.ordenacao import ordenar_produtos_por_id
from estruturas.fila import Fila
from estruturas.lde import LDE
from estruturas.lse import LSE
from estruturas.pilha import Pilha
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from services.persistencia_service import PersistenciaService


class EstoqueService:
    def __init__(self, pasta_data=None):
        if pasta_data is None:
            pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pasta_data = os.path.join(pasta_raiz, "data")

        self.clientes = LSE()
        self.produtos = LDE()
        self.vendas = Fila()
        self.historico = Pilha()
        self.persistencia = PersistenciaService(pasta_data)

        self.carregar_dados()

    def carregar_dados(self):
        for cliente in self.persistencia.carregar_clientes():
            if self.clientes.buscar(cliente.codigo) is None:
                self.clientes.inserir_fim(cliente)
            else:
                print(f"Aviso: cliente com ID duplicado foi ignorado: {cliente.codigo}.")

        for produto in self.persistencia.carregar_produtos():
            if self.produtos.buscar(produto.codigo) is None:
                self.produtos.inserir_fim(produto)
            else:
                print(f"Aviso: produto com ID duplicado foi ignorado: {produto.codigo}.")

        codigos_vendas = {venda.codigo for venda in self.vendas.listar()}

        for venda in self.persistencia.carregar_vendas():
            if venda.codigo in codigos_vendas:
                print(f"Aviso: venda com ID duplicado foi ignorada: {venda.codigo}.")
                continue

            if self.clientes.buscar(venda.codigo_cliente) is None:
                print(
                    f"Aviso: venda {venda.codigo} ignorada porque o cliente "
                    f"{venda.codigo_cliente} nao existe."
                )
                continue

            produto_inexistente = None

            for item in venda.itens:
                if self.produtos.buscar(item["codigo_produto"]) is None:
                    produto_inexistente = item["codigo_produto"]
                    break

            if produto_inexistente is not None:
                print(
                    f"Aviso: venda {venda.codigo} ignorada porque o produto "
                    f"{produto_inexistente} nao existe."
                )
                continue

            self.vendas.enqueue(venda)
            codigos_vendas.add(venda.codigo)

    def gerar_proximo_codigo_cliente(self):
        return self._gerar_proximo_codigo(self.clientes.listar())

    def gerar_proximo_codigo_produto(self):
        return self._gerar_proximo_codigo(self.produtos.listar())

    def gerar_proximo_codigo_venda(self):
        return self._gerar_proximo_codigo(self.vendas.listar())

    def _gerar_proximo_codigo(self, registros):
        maior_codigo = 0

        for registro in registros:
            if registro.codigo > maior_codigo:
                maior_codigo = registro.codigo

        return maior_codigo + 1

    def _validar_codigo(self, codigo, nome_campo="ID"):
        if isinstance(codigo, bool):
            raise ValueError(f"O {nome_campo} deve ser um numero inteiro.")

        try:
            codigo_convertido = int(codigo)
        except (OverflowError, TypeError, ValueError):
            raise ValueError(f"O {nome_campo} deve ser um numero inteiro.")

        if isinstance(codigo, float) and not codigo.is_integer():
            raise ValueError(f"O {nome_campo} deve ser um numero inteiro.")

        if codigo_convertido <= 0:
            raise ValueError(f"O {nome_campo} deve ser maior que zero.")

        return codigo_convertido

    def _validar_quantidade(self, quantidade, permite_zero):
        if isinstance(quantidade, bool):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        try:
            quantidade_convertida = int(quantidade)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if isinstance(quantidade, float) and not quantidade.is_integer():
            raise ValueError("A quantidade deve ser um numero inteiro.")

        if permite_zero and quantidade_convertida < 0:
            raise ValueError("A quantidade nao pode ser negativa.")

        if not permite_zero and quantidade_convertida <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        return quantidade_convertida

    def _buscar_posicao(self, registros, codigo):
        for posicao, registro in enumerate(registros):
            if registro.codigo == codigo:
                return posicao

        return -1

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
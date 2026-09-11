import os

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

    def realizar_venda(self, codigo_cliente, itens):
        codigo_cliente = self._validar_codigo(codigo_cliente, "ID do cliente")

        if self.clientes.buscar(codigo_cliente) is None:
            raise ValueError("Cliente nao encontrado.")

        if not isinstance(itens, list) or len(itens) == 0:
            raise ValueError("A venda deve possuir pelo menos um produto.")

        quantidades_por_produto = {}

        for item in itens:
            if not isinstance(item, dict):
                raise ValueError("Item de venda invalido.")

            try:
                codigo_produto = self._validar_codigo(
                    item["codigo_produto"], "ID do produto"
                )
                quantidade = self._validar_quantidade(
                    item["quantidade"], permite_zero=False
                )
            except KeyError:
                raise ValueError("Item de venda invalido.")

            quantidade_atual = quantidades_por_produto.get(codigo_produto, 0)
            quantidades_por_produto[codigo_produto] = quantidade_atual + quantidade

        itens_da_venda = []

        for codigo_produto, quantidade in quantidades_por_produto.items():
            produto = self.produtos.buscar(codigo_produto)

            if produto is None:
                raise ValueError(f"Produto {codigo_produto} nao encontrado.")

            if produto.quantidade < quantidade:
                raise ValueError(
                    f"Estoque insuficiente para o produto {produto.nome}. "
                    f"Disponivel: {produto.quantidade}."
                )

            itens_da_venda.append(
                {
                    "codigo_produto": codigo_produto,
                    "quantidade": quantidade,
                    "preco_unitario": produto.preco,
                }
            )

        venda = Venda(
            self.gerar_proximo_codigo_venda(),
            codigo_cliente,
            itens_da_venda,
        )

        for item in itens_da_venda:
            produto = self.produtos.buscar(item["codigo_produto"])
            produto.atualizar_estoque(produto.quantidade - item["quantidade"])

        self.vendas.enqueue(venda)

        try:
            self.salvar_produtos()
            self.salvar_vendas()
        except OSError:
            self.vendas.remover_ultima()

            for item in itens_da_venda:
                produto = self.produtos.buscar(item["codigo_produto"])
                produto.atualizar_estoque(produto.quantidade + item["quantidade"])

            self.salvar_produtos()
            self.salvar_vendas()
            raise

        self.historico.push({"tipo": "venda", "venda": venda})
        return venda

    def realizar_venda_exemplo(self, codigo_cliente, codigo_produto, quantidade):
        itens = [
            {
                "codigo_produto": codigo_produto,
                "quantidade": quantidade,
            }
        ]
        return self.realizar_venda(codigo_cliente, itens)

    def listar_vendas(self):
        return self.vendas.listar()

    def primeira_venda(self):
        return self.vendas.front()

    def valor_total_estoque(self):
        total = 0.0

        for produto in self.produtos.listar():
            total += produto.preco * produto.quantidade

        return round(total, 2)

    def valor_total_vendas(self):
        total = 0.0

        for venda in self.vendas.listar():
            total += venda.valor_total

        return round(total, 2)

    def clientes_e_valores_totais_gastos(self):
        totais_por_cliente = {}

        for venda in self.vendas.listar():
            total_atual = totais_por_cliente.get(venda.codigo_cliente, 0.0)
            totais_por_cliente[venda.codigo_cliente] = total_atual + venda.valor_total

        clientes_e_totais = []

        for cliente in self.clientes.listar():
            total = totais_por_cliente.get(cliente.codigo, 0.0)
            clientes_e_totais.append((cliente, round(total, 2)))

        return clientes_e_totais

    def cliente_que_mais_gastou(self):
        if self.vendas.is_empty():
            return None

        maior_resultado = None

        for cliente, total in self.clientes_e_valores_totais_gastos():
            if maior_resultado is None or total > maior_resultado[1]:
                maior_resultado = (cliente, total)

        if maior_resultado is None or maior_resultado[1] == 0:
            return None

        return maior_resultado

    def produto_mais_vendido(self):
        if self.vendas.is_empty():
            return None

        quantidades_vendidas = {}

        for venda in self.vendas.listar():
            for item in venda.itens:
                codigo_produto = item["codigo_produto"]
                quantidade_atual = quantidades_vendidas.get(codigo_produto, 0)
                quantidades_vendidas[codigo_produto] = (
                    quantidade_atual + item["quantidade"]
                )

        resultado = None

        for produto in self.produtos.listar():
            quantidade = quantidades_vendidas.get(produto.codigo, 0)

            if quantidade > 0 and (resultado is None or quantidade > resultado[1]):
                resultado = (produto, quantidade)

        return resultado

    def desfazer_ultima_operacao(self):
        operacao = self.historico.pop()
        tipo = operacao["tipo"]

        if tipo == "cadastro_cliente":
            cliente = operacao["cliente"]
            self.clientes.remover(cliente.codigo)

            try:
                self.salvar_clientes()
            except OSError:
                self.clientes.inserir_posicao(operacao["posicao"], cliente)
                self.historico.push(operacao)
                raise

            return f"Cadastro do cliente {cliente.nome} desfeito."

        if tipo == "remocao_cliente":
            cliente = operacao["cliente"]
            self.clientes.inserir_posicao(operacao["posicao"], cliente)

            try:
                self.salvar_clientes()
            except OSError:
                self.clientes.remover(cliente.codigo)
                self.historico.push(operacao)
                raise

            return f"Remocao do cliente {cliente.nome} desfeita."

        if tipo == "cadastro_produto":
            produto = operacao["produto"]
            self.produtos.remover(produto.codigo)

            try:
                self.salvar_produtos()
            except OSError:
                self.produtos.inserir_posicao(operacao["posicao"], produto)
                self.historico.push(operacao)
                raise

            return f"Cadastro do produto {produto.nome} desfeito."

        if tipo == "remocao_produto":
            produto = operacao["produto"]
            self.produtos.inserir_posicao(operacao["posicao"], produto)

            try:
                self.salvar_produtos()
            except OSError:
                self.produtos.remover(produto.codigo)
                self.historico.push(operacao)
                raise

            return f"Remocao do produto {produto.nome} desfeita."

        if tipo == "atualizacao_estoque":
            produto = operacao["produto"]
            produto.atualizar_estoque(operacao["quantidade_anterior"])

            try:
                self.salvar_produtos()
            except OSError:
                produto.atualizar_estoque(operacao["quantidade_nova"])
                self.historico.push(operacao)
                raise

            return f"Atualizacao do estoque de {produto.nome} desfeita."

        if tipo == "venda":
            venda = operacao["venda"]
            ultima_venda = self.vendas.remover_ultima()

            if ultima_venda.codigo != venda.codigo:
                self.vendas.enqueue(ultima_venda)
                self.historico.push(operacao)
                raise ValueError("Nao foi possivel localizar a ultima venda.")

            produtos_restaurados = []

            for item in venda.itens:
                produto = self.produtos.buscar(item["codigo_produto"])

                if produto is None:
                    for produto_anterior, quantidade in produtos_restaurados:
                        produto_anterior.atualizar_estoque(
                            produto_anterior.quantidade - quantidade
                        )

                    self.vendas.enqueue(venda)
                    self.historico.push(operacao)
                    raise ValueError(
                        f"Produto {item['codigo_produto']} da venda nao foi encontrado."
                    )

                produto.atualizar_estoque(produto.quantidade + item["quantidade"])
                produtos_restaurados.append((produto, item["quantidade"]))

            try:
                self.salvar_produtos()
                self.salvar_vendas()
            except OSError as erro:
                for produto, quantidade in produtos_restaurados:
                    produto.atualizar_estoque(produto.quantidade - quantidade)

                self.vendas.enqueue(venda)
                self.historico.push(operacao)

                try:
                    self.salvar_produtos()
                except OSError:
                    print("Aviso: nao foi possivel restaurar o arquivo de produtos.")

                try:
                    self.salvar_vendas()
                except OSError:
                    print("Aviso: nao foi possivel restaurar o arquivo de vendas.")

                raise erro

            return f"Venda {venda.codigo} desfeita."

        self.historico.push(operacao)
        raise ValueError("Operacao desconhecida no historico.")

    def salvar_clientes(self):
        self.persistencia.salvar_clientes(self.clientes.listar())

    def salvar_produtos(self):
        self.persistencia.salvar_produtos(self.produtos.listar())

    def salvar_vendas(self):
        self.persistencia.salvar_vendas(self.vendas.listar())
import math
import os

from services.estoque_service import EstoqueService


def ler_inteiro(mensagem):
    texto = input(mensagem).strip()

    if texto == "":
        raise ValueError("Digite um numero inteiro.")

    try:
        return int(texto)
    except ValueError:
        raise ValueError("Digite um numero inteiro valido.")


def ler_float(mensagem):
    texto = input(mensagem).strip().replace(",", ".")

    if texto == "":
        raise ValueError("Digite um numero.")

    try:
        valor = float(texto)
    except ValueError:
        raise ValueError("Digite um numero valido.")

    if not math.isfinite(valor):
        raise ValueError("Digite um numero finito.")

    return valor


def ler_texto_obrigatorio(mensagem):
    texto = input(mensagem).strip()

    if texto == "":
        raise ValueError("O campo nao pode ficar vazio.")

    return texto


def pausar():
    input("\nPressione ENTER para continuar...")


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_registros(registros, mensagem_vazia):
    if len(registros) == 0:
        print(mensagem_vazia)
        return

    for registro in registros:
        print(registro)


def exibir_menu():
    print("\n==============================")
    print("SISTEMA DE ESTOQUE E VENDAS")
    print("==============================")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Buscar cliente")
    print("4 - Remover cliente")
    print("5 - Cadastrar produto")
    print("6 - Listar produtos")
    print("7 - Buscar produto")
    print("8 - Atualizar estoque")
    print("9 - Remover produto")
    print("10 - Listar produtos em ordem inversa")
    print("11 - Listar produtos ordenados por ID")
    print("12 - Buscar produto por ID usando Busca Binaria")
    print("13 - Realizar venda")
    print("14 - Visualizar fila de vendas")
    print("15 - Visualizar primeira venda da fila")
    print("16 - Exibir valor total do estoque")
    print("17 - Exibir valor total das vendas")
    print("18 - Exibir clientes e valores totais gastos")
    print("19 - Exibir cliente que mais gastou")
    print("20 - Exibir produto mais vendido")
    print("21 - Desfazer ultima operacao")
    print("0 - Sair")

    if opcao == 1:
        nome = ler_texto_obrigatorio("Nome do cliente: ")
        cliente = service.cadastrar_cliente(nome)
        print(f"Cliente cadastrado com sucesso: {cliente}")

    elif opcao == 2:
        imprimir_registros(
            service.listar_clientes(),
            "Nenhum cliente cadastrado.",
        )

    elif opcao == 3:
        codigo = ler_inteiro("ID do cliente: ")
        cliente = service.buscar_cliente(codigo)

        if cliente is None:
            print("Cliente nao encontrado.")
        else:
            print(cliente)

    elif opcao == 4:
        codigo = ler_inteiro("ID do cliente que sera removido: ")
        cliente = service.remover_cliente(codigo)
        print(f"Cliente removido com sucesso: {cliente}")

    
    elif opcao == 5:
        nome = ler_texto_obrigatorio("Nome do produto: ")
        preco = ler_float("Preco do produto: R$ ")
        quantidade = ler_inteiro("Quantidade em estoque: ")
        produto = service.cadastrar_produto(nome, preco, quantidade)
        print(f"Produto cadastrado com sucesso: {produto}")

    elif opcao == 6:
        imprimir_registros(
            service.listar_produtos(),
            "Nenhum produto cadastrado.",
        )

    elif opcao == 7:
        codigo = ler_inteiro("ID do produto: ")
        produto = service.buscar_produto(codigo)

        if produto is None:
            print("Produto nao encontrado.")
        else:
            print(produto)

    elif opcao == 8:
        codigo = ler_inteiro("ID do produto: ")
        quantidade = ler_inteiro("Nova quantidade em estoque: ")
        produto = service.atualizar_estoque(codigo, quantidade)
        print(f"Estoque atualizado com sucesso: {produto}")

    elif opcao == 9:
        codigo = ler_inteiro("ID do produto que sera removido: ")
        produto = service.remover_produto(codigo)
        print(f"Produto removido com sucesso: {produto}")

    elif opcao == 10:
        imprimir_registros(
            service.listar_produtos_inverso(),
            "Nenhum produto cadastrado.",
        )
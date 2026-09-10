def buscar_produto_por_id(produtos_ordenados, codigo):
    inicio = 0
    fim = len(produtos_ordenados) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        produto_do_meio = produtos_ordenados[meio]

        if produto_do_meio.codigo == codigo:
            return produto_do_meio

        if codigo < produto_do_meio.codigo:
            fim = meio - 1
        else:
            inicio = meio + 1

    return None
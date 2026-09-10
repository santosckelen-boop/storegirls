def ordenar_produtos_por_id(produtos):
    produtos_ordenados = list(produtos)

    for i in range(1, len(produtos_ordenados)):
        valor_atual = produtos_ordenados[i]
        valor_anterior = i - 1

        while (
            valor_anterior >= 0
            and produtos_ordenados[valor_anterior].codigo > valor_atual.codigo
        ):
            produtos_ordenados[valor_anterior + 1] = produtos_ordenados[valor_anterior]
            valor_anterior -= 1

        produtos_ordenados[valor_anterior + 1] = valor_atual

    return produtos_ordenados
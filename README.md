    # Girls'shop

    Descrição

    O GirlsShop é um sistema de gerenciamento de uma loja desenvolvido em Python, funcionando pelo terminal. O sistema permite cadastrar clientes e produtos, controlar o estoque, realizar vendas e consultar informações da loja.

    Objetivo

    O projeto tem como objetivo aplicar os conceitos de Estruturas de Dados, Algoritmos e Programação Orientada a Objetos, desenvolvidos durante a disciplina.

    Tecnologias

    * Python 3
    * Git e GitHub
    * Arquivos CSV para armazenamento dos dados

    Estruturas e Algoritmos

    Foram utilizadas as seguintes estruturas de dados:

    * Lista Simplesmente Encadeada (LSE): gerenciamento dos clientes;
    * Lista Duplamente Encadeada (LDE): gerenciamento dos produtos;
    * Fila: armazenamento das vendas;
    * Pilha: histórico de operações e função de desfazer.

    Também foram utilizados:

    * Insertion Sort: ordenação dos produtos por ID;
    * Busca Binária: busca de produtos pelo ID.

    Funcionalidades

    O sistema permite:

    * Cadastrar, listar, buscar e remover clientes;
    * Cadastrar, listar, buscar e remover produtos;
    * Atualizar o estoque;
    * Listar produtos em ordem inversa;
    * Ordenar produtos por ID;
    * Buscar produtos utilizando Busca Binária;
    * Realizar vendas;
    * Visualizar a fila de vendas;
    * Consultar o valor total do estoque;
    * Consultar o valor total das vendas;
    * Ver os clientes que mais gastaram;
    * Ver o produto mais vendido;
    * Desfazer a última operação.

    Como executar

    É necessário ter o Python 3 instalado.

    No terminal, dentro da pasta do projeto, execute:

    python main.py

    O sistema será iniciado no terminal e apresentará o menu com as opções disponíveis.

    Organização

    GirlsShop/
    ├── algoritmos/
    ├── estruturas/
    ├── models/
    ├── services/
    ├── data/
    ├── main.py
    └── README.md

    * algoritmos/ → algoritmos de ordenação e busca;
    * estruturas/ → estruturas de dados;
    * models/ → classes de clientes, produtos e vendas;
    * services/ → regras do sistema e persistência;
    * data/ → arquivos CSV;
    * main.py → arquivo principal do sistema.

    Persistência

    Os dados são armazenados em arquivos CSV dentro da pasta data/:

    * clientes.csv
    * produtos.csv
    * vendas.csv

    Ao iniciar o sistema, os dados são carregados dos arquivos. As alterações realizadas são salvas automaticamente, permitindo que as informações permaneçam disponíveis mesmo após fechar o programa.

    Integrantes

   * 1139889 - Allana Prestes
   * 1140047 - Caroline Russo Zilio
   * 1139521 - Eloise Pagnussat
   * 1102339 - Kélen Camargo dos Santos
   * 1139749 - Luísa Lima Migliorini
   * 1139410 - Vitória Drechsler 

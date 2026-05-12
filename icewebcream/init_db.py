import sqlite3

def init_db():
    # 1. Conecta ao banco (isso cria o arquivo database.db se ele não existir)
    connection = sqlite3.connect('database.db')

    # 2. Lê e executa o seu schema.sql
    with open('schema.sql', encoding='utf-8') as f:
        connection.executescript(f.read())

    cursor = connection.cursor()

    # --- INJETANDO DADOS FICTÍCIOS (SEED) ---

    # Categorias
    cursor.execute("INSERT INTO categorias (nome) VALUES ('Frutas')")
    cursor.execute("INSERT INTO categorias (nome) VALUES ('Embalagens')")

    # Fornecedores (Os mesmos do seu protótipo)
    cursor.execute("INSERT INTO fornecedores (nome, contato) VALUES ('Sacolão do Alfase', '11999999999')")
    cursor.execute("INSERT INTO fornecedores (nome, contato) VALUES ('Massa Viva', '11888888888')")

    # Produtos
    # Abacaxi: categoria 1 (Frutas), fornecedor 1 (Sacolão)
    cursor.execute("""
        INSERT INTO produtos (sku, descricao, categoria_id, fornecedor_id, unidade_medida, estoque_minimo)
        VALUES ('FRU001', 'Abacaxi', 1, 1, 'Kg', 7)
    """)
    # Casquinha: categoria 2 (Embalagens), fornecedor 2 (Massa Viva)
    cursor.execute("""
        INSERT INTO produtos (sku, descricao, categoria_id, fornecedor_id, unidade_medida, estoque_minimo)
        VALUES ('EMB001', 'Casquinha', 2, 2, 'unidades', 50)
    """)

    # --- TESTANDO AS SUAS TRIGGERS ---
    
    # Produto 1 (Abacaxi): Vamos dar ENTRADA de 10 Kg, e SAÍDA de 8 Kg. A trigger tem que deixar o estoque em 2.
    cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao) VALUES (1, 'entrada', 10, 'Compra da semana')")
    cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao) VALUES (1, 'saida', 8, 'Consumo')")

    # Produto 2 (Casquinha): Vamos usar o tipo AJUSTE para definir o estoque direto para 7.
    cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao) VALUES (2, 'ajuste', 7, 'Contagem de Terça-feira')")

    # Salva as alterações e fecha a conexão
    connection.commit()
    connection.close()
    
    print("Banco de dados criado e populado com sucesso! Triggers ativadas.")

if __name__ == '__main__':
    init_db()
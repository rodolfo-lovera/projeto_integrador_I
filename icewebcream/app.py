from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota da página inicial
@app.route('/')
def index():
    conn = get_db_connection()
    produtos_estoque = conn.execute('''
        SELECT p.descricao, e.quantidade, p.estoque_minimo
        FROM produtos p
        JOIN estoque e ON p.id = e.produto_id
    ''').fetchall()
    conn.close()
    
    # Agora chamamos o HTML ao invés de escrever aqui
    return render_template('index.html', produtos=produtos_estoque)

# Rota de Cadastro (Aceita GET para exibir a tela e POST para salvar os dados)
@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    conn = get_db_connection()
    
    # Se o usuário clicou no botão "Salvar Produto"
    if request.method == 'POST':
        sku = request.form['sku']
        descricao = request.form['descricao']
        categoria_id = request.form['categoria_id']
        fornecedor_id = request.form['fornecedor_id']
        unidade_medida = request.form['unidade_medida']
        estoque_minimo = request.form['estoque_minimo']

        # Insere no banco de dados
        conn.execute('''
            INSERT INTO produtos (sku, descricao, categoria_id, fornecedor_id, unidade_medida, estoque_minimo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sku, descricao, categoria_id, fornecedor_id, unidade_medida, estoque_minimo))
        conn.commit()
        conn.close()
        
        # Redireciona de volta para a tela inicial
        return redirect(url_for('index'))

    # Se for apenas GET (usuário apenas abriu a tela)
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    fornecedores = conn.execute('SELECT * FROM fornecedores').fetchall()
    conn.close()
    
    return render_template('cadastro_produto.html', categorias=categorias, fornecedores=fornecedores)

# Rota de Movimentação de Estoque
@app.route('/movimentacao', methods=('GET', 'POST'))
def movimentacao():
    conn = get_db_connection()
    
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        tipo = request.form['tipo']
        quantidade = request.form['quantidade']
        observacao = request.form['observacao']

        # O Python APENAS insere a movimentação. O SQLite vai disparar a Trigger e atualizar a tabela 'estoque' sozinho!
        conn.execute('''
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
            VALUES (?, ?, ?, ?)
        ''', (produto_id, tipo, quantidade, observacao))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))

    # Se for GET, busca apenas os produtos ativos para mostrar no Dropdown
    produtos = conn.execute('SELECT id, descricao FROM produtos WHERE ativo = 1').fetchall()
    conn.close()
    
    return render_template('movimentacao.html', produtos=produtos)

# Rota do Relatório de Compras
@app.route('/compras')
def compras():
    conn = get_db_connection()
    
    # A consulta SQL inteligente: junta produtos, estoque e fornecedores, 
    # e filtra (WHERE) apenas os que estão abaixo do mínimo.
    lista_compras = conn.execute('''
        SELECT 
            f.nome as fornecedor_nome,
            p.descricao,
            p.unidade_medida,
            e.quantidade,
            p.estoque_minimo,
            (p.estoque_minimo - e.quantidade) as quantidade_a_comprar
        FROM produtos p
        JOIN estoque e ON p.id = e.produto_id
        JOIN fornecedores f ON p.fornecedor_id = f.id
        WHERE e.quantidade < p.estoque_minimo
        ORDER BY f.nome
    ''').fetchall()
    
    conn.close()
    
    return render_template('compras.html', lista_compras=lista_compras)

if __name__ == '__main__':
    app.run(debug=True)
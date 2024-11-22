from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from models import db, Produto, MovimentacaoEstoque  # Importando o banco de dados e os modelos
from forms import ProdutoForm  # Importando o formulário ProdutoForm

# Configuração do aplicativo Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'  # Chave secreta para mensagens flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Configuração do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o banco de dados

# Defina as rotas aqui
@app.route('/')
def home():
    return render_template('home.html')  # Página inicial com navbar

# Rota para a lista de produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()  # Busca todos os produtos do banco
    return render_template('listar_produtos.html', produtos=produtos)

# Rota para a página de controle de estoque
@app.route('/estoque')
def estoque():
    movimentacoes = MovimentacaoEstoque.query.order_by(MovimentacaoEstoque.data.desc()).all()
    print("Movimentações: ", movimentacoes)  # Verifique o conteúdo no console
    return render_template('estoque.html', movimentacoes=movimentacoes)

# Rota para adicionar produto
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    form = ProdutoForm()

    if form.validate_on_submit():  # Verifica se o formulário foi enviado corretamente
        # Coletar os dados do formulário
        codigo = form.codigo.data
        nome = form.nome.data
        marca = form.marca.data
        categoria = form.categoria.data
        quantidade = form.quantidade.data
        preco = form.preco.data
        localizacao = form.localizacao.data

        # Criar uma instância do produto
        novo_produto = Produto(
            codigo=codigo,
            nome=nome,
            marca=marca,
            categoria=categoria,
            quantidade=quantidade,
            preco=preco,
            localizacao=localizacao
        )

        # Adicionar ao banco de dados
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto adicionado com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('listar_produtos'))

    return render_template('adicionar_produto.html', form=form)

# Rota para remover produto
@app.route('/remover/<int:id>', methods=['POST'])
def remover_produto(id):
    produto = Produto.query.get_or_404(id)  # Busca o produto pelo ID
    db.session.delete(produto)  # Remove o produto do banco
    db.session.commit()  # Confirma a remoção no banco

    flash('Produto removido com sucesso!', 'success')  # Mensagem de sucesso
    return redirect(url_for('listar_produtos'))  # Redireciona para a lista de produtos

# Rota para Editar Produto
@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)  # Buscar o produto pelo ID

    # Preencher o formulário com os dados atuais do produto
    form = ProdutoForm(obj=produto)

    if form.validate_on_submit():  # Quando o formulário for enviado corretamente
        produto.codigo = form.codigo.data
        produto.nome = form.nome.data
        produto.marca = form.marca.data
        produto.categoria = form.categoria.data
        produto.quantidade = form.quantidade.data
        produto.preco = form.preco.data
        produto.localizacao = form.localizacao.data

        db.session.commit()  # Salva as alterações no banco de dados

        flash('Produto atualizado com sucesso!', 'success')  # Mensagem de sucesso
        return redirect(url_for('listar_produtos'))  # Redireciona para a lista de produtos

    return render_template('editar_produto.html', form=form, produto=produto)

# Rota para Entrada no Estoque
@app.route('/estoque/entrada', methods=['GET', 'POST'])
def entrada_estoque():
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])  # Garantir que o produto_id é um inteiro
        quantidade = int(request.form['quantidade'])

        # Registrar a movimentação de entrada
        movimentacao = MovimentacaoEstoque(produto_id=produto_id, quantidade=quantidade, tipo='entrada')
        db.session.add(movimentacao)
        db.session.commit()

        # Atualizar a quantidade do produto
        produto = Produto.query.get_or_404(produto_id)
        produto.quantidade += quantidade  # Incrementa a quantidade no estoque
        db.session.commit()

        flash(f'Entrada registrada com sucesso para o produto {produto.nome}!', 'success')
        return redirect(url_for('estoque'))
    
    produtos = Produto.query.all()
    return render_template('entrada_estoque.html', produtos=produtos)

# Rota para Saída no Estoque
@app.route('/estoque/saida', methods=['GET', 'POST'])
def saida_estoque():
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])  # Garantir que o produto_id é um inteiro
        quantidade = int(request.form['quantidade'])

        # Registrar a movimentação de saída
        movimentacao = MovimentacaoEstoque(produto_id=produto_id, quantidade=quantidade, tipo='saida')
        db.session.add(movimentacao)
        db.session.commit()

        # Atualizar a quantidade do produto
        produto = Produto.query.get_or_404(produto_id)
        if produto.quantidade >= quantidade:  # Verifica se a quantidade em estoque é suficiente
            produto.quantidade -= quantidade  # Decrementa a quantidade no estoque
            db.session.commit()
            flash('Saída registrada com sucesso!', 'success')
        else:
            flash('Quantidade insuficiente em estoque.', 'error')

        return redirect(url_for('estoque'))

    produtos = Produto.query.all()
    return render_template('saida_estoque.html', produtos=produtos)

# Rota para API de produtos
@app.route('/api/produtos', methods=['GET'])
def api_listar_produtos():
    produtos = Produto.query.all()  # Busca todos os produtos do banco
    produtos_json = [
        {
            'codigo': produto.codigo,
            'nome': produto.nome,
            'categoria': produto.categoria,
            'quantidade': produto.quantidade,
            'preco': produto.preco,
            'localizacao': produto.localizacao
        }
        for produto in produtos
    ]
    return jsonify(produtos_json)

# Só vai rodar a aplicação Flask aqui se o script for executado diretamente
if __name__ == '__main__':
    with app.app_context():  # Garante que o contexto da aplicação esteja presente
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)

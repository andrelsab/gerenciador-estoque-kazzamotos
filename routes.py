from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Produto  # Importando o banco de dados e o modelo Produto
from forms import ProdutoForm  # Importando o formulário ProdutoForm

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Necessária para mensagens flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o banco de dados

# Rota Home
@app.route('/')
def home():
    return render_template('home.html')

# Rota Produtos - Exibir lista de produtos
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

# Rota para Adicionar Produto
@app.route('/produtos/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    form = ProdutoForm()  # Inicializa o formulário

    if form.validate_on_submit():  # Quando o formulário for enviado corretamente
        # Captura os dados do formulário
        codigo = form.codigo.data
        nome = form.nome.data
        marca = form.marca.data
        categoria = form.categoria.data
        quantidade = form.quantidade.data
        preco = form.preco.data
        localizacao = form.localizacao.data

        # Cria um novo produto
        novo_produto = Produto(
            codigo=codigo,
            nome=nome,
            marca=marca,
            categoria=categoria,
            quantidade=quantidade,
            preco=preco,
            localizacao=localizacao
        )

        # Adiciona o produto ao banco de dados
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))

    return render_template('adicionar_produto.html', form=form)

# Rota para Remover Produto
@app.route('/produtos/remover/<int:id>', methods=['POST'])
def remover_produto(id):
    produto = Produto.query.get_or_404(id)  # Busca o produto pelo ID ou retorna 404 se não encontrado
    
    # Deleta o produto do banco de dados
    db.session.delete(produto)
    db.session.commit()

    flash('Produto removido com sucesso!', 'success')
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


# Rota Estoque - Página inicial para entrada e saída
@app.route('/estoque')
def estoque():
    return render_template('estoque.html')

# Rota para Entrada no Estoque
@app.route('/estoque/entrada', methods=['GET', 'POST'])
def entrada_estoque():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])

        produto = Produto.query.get_or_404(produto_id)
        produto.quantidade += quantidade
        db.session.commit()

        flash('Entrada registrada com sucesso!', 'success')
        return redirect(url_for('estoque'))

    produtos = Produto.query.all()
    return render_template('entrada_estoque.html', produtos=produtos)

# Rota para Saída no Estoque
@app.route('/estoque/saida', methods=['GET', 'POST'])
def saida_estoque():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])

        produto = Produto.query.get_or_404(produto_id)
        if produto.quantidade >= quantidade:
            produto.quantidade -= quantidade
            db.session.commit()
            flash('Saída registrada com sucesso!', 'success')
        else:
            flash('Quantidade insuficiente em estoque.', 'error')

        return redirect(url_for('estoque'))

    produtos = Produto.query.all()
    return render_template('saida_estoque.html', produtos=produtos)

# Inicializa o servidor
if __name__ == '__main__':
    app.run(debug=True)

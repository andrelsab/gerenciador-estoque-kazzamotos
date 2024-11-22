from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa o objeto de banco de dados
db = SQLAlchemy()

# Modelo Produto
class Produto(db.Model):
    # Definição da tabela
    __tablename__ = 'produtos'

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # Código único do produto
    nome = db.Column(db.String(100), nullable=False)  # Nome do produto
    marca = db.Column(db.String(50), nullable=False)  # Marca do produto
    categoria = db.Column(db.String(50), nullable=False)  # Categoria do produto
    quantidade = db.Column(db.Integer, nullable=False)  # Quantidade em estoque
    preco = db.Column(db.Float, nullable=False)  # Preço do produto
    localizacao = db.Column(db.String(100), nullable=True)  # Localização do produto no estoque
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação do registro
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização

    # Relacionamento com MovimentacaoEstoque
    movimentacoes = db.relationship(
        'MovimentacaoEstoque',
        backref='produto',
        lazy=True,
        cascade="all, delete-orphan"  # Permite a exclusão em cascata
    )

    def __repr__(self):
        """Representação legível do objeto Produto."""
        return f'<Produto {self.nome} (Código: {self.codigo})>'

    # Método para converter o objeto em dicionário (útil para APIs)
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'marca': self.marca,
            'categoria': self.categoria,
            'quantidade': self.quantidade,
            'preco': self.preco,
            'localizacao': self.localizacao,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat(),
        }

    # Método estático para criar um produto a partir de um dicionário (útil para APIs ou processamento de formulários)
    @staticmethod
    def from_dict(data):
        return Produto(
            codigo=data.get('codigo'),
            nome=data.get('nome'),
            marca=data.get('marca'),
            categoria=data.get('categoria'),
            quantidade=data.get('quantidade'),
            preco=data.get('preco'),
            localizacao=data.get('localizacao')
        )


# Modelo MovimentacaoEstoque
class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # Pode ser 'entrada' ou 'saida'
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MovimentacaoEstoque {self.tipo} produto {self.produto.nome if self.produto else "N/A"} em {self.data}>'

    # Método para converter o objeto em dicionário (útil para APIs)
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'tipo': self.tipo,
            'data': self.data.isoformat(),
        }

    # Método estático para criar uma movimentação de estoque a partir de um dicionário
    @staticmethod
    def from_dict(data):
        return MovimentacaoEstoque(
            produto_id=data.get('produto_id'),
            quantidade=data.get('quantidade'),
            tipo=data.get('tipo')
        )

# setup_db.py
from app import db  # Importa o db, mas não o app que registra as rotas
from models import Produto, MovimentacaoEstoque  # Importa os modelos

# Certifique-se de que o contexto da aplicação Flask esteja presente para criar as tabelas
from app import app

with app.app_context():  # Usa o contexto da aplicação Flask
    db.create_all()  # Cria as tabelas no banco de dados

print("Banco de dados configurado com sucesso!")

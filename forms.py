from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

class ProdutoForm(FlaskForm):
    # Campo para o código do produto
    codigo = StringField(
        'Código', 
        validators=[
            DataRequired(message="O código é obrigatório."),
            Length(max=10, message="O código deve ter no máximo 10 caracteres.")
        ]
    )

    # Campo para o nome do produto
    nome = StringField(
        'Nome', 
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(max=50, message="O nome deve ter no máximo 50 caracteres.")
        ]
    )

    # Campo para a marca do produto
    marca = StringField(
        'Marca', 
        validators=[
            DataRequired(message="A marca é obrigatória."),
            Length(max=30, message="A marca deve ter no máximo 30 caracteres.")
        ]
    )

    # Campo para a categoria do produto
    categoria = StringField(
        'Categoria', 
        validators=[
            DataRequired(message="A categoria é obrigatória."),
            Length(max=30, message="A categoria deve ter no máximo 30 caracteres.")
        ]
    )

    # Campo para a quantidade do produto
    quantidade = IntegerField(
        'Quantidade', 
        validators=[
            DataRequired(message="A quantidade é obrigatória."),
            NumberRange(min=1, message="A quantidade deve ser maior ou igual a 1.")
        ]
    )

    # Campo para o preço do produto
    preco = DecimalField(
        'Preço', 
        validators=[
            DataRequired(message="O preço é obrigatório."),
            NumberRange(min=0.01, message="O preço deve ser maior que 0.")
        ]
    )

    # Campo para a localização do produto
    localizacao = StringField(
        'Localização', 
        validators=[
            DataRequired(message="A localização é obrigatória."),
            Length(max=20, message="A localização deve ter no máximo 20 caracteres.")
        ]
    )

    # Método opcional para validações personalizadas (exemplo)
    def validate_codigo(self, field):
        if not field.data.isalnum():
            raise ValidationError("O código deve conter apenas letras e números.")

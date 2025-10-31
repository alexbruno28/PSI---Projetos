from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from models.user import User 




class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message='Obrigatório'),
        Length(min=4, max=80, message='4 a 80 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Obrigatório')
    ])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message='Obrigatório'),
        Length(min=4, max=80, message='4 a 80 caracteres')
    ])
    email = StringField('E-mail', validators=[
        DataRequired(message='Obrigatório'),
        Email(message='E-mail inválido'),
        Length(max=120)
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Obrigatório'),
        Length(min=6, message='Mínimo 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Obrigatório'),
        EqualTo('password', message='Senhas não conferem')
    ])
    submit = SubmitField('Registrar')

    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Nome de usuário já em uso.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('E-mail já cadastrado.')


class ProductForm(FlaskForm):
    name = StringField('Nome do Produto', validators=[
        DataRequired(message='Obrigatório'),
        Length(min=2, max=100, message='2 a 100 caracteres')
    ])
    description = TextAreaField('Descrição', validators=[
        Length(max=500, message='Máximo 500 caracteres.')
    ])
    price = DecimalField('Preço', validators=[
        DataRequired(message='Obrigatório'),
        NumberRange(min=0.01, message='Maior que zero')
    ])
    submit = SubmitField('Salvar')
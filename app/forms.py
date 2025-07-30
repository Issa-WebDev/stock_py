from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from app.models import User, Product

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(), 
        Length(min=4, max=20, message='Le nom d\'utilisateur doit contenir entre 4 et 20 caractères')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    password2 = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField('S\'inscrire')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ProductForm(FlaskForm):
    name = StringField('Nom du produit', validators=[DataRequired(), Length(max=100)])
    reference = StringField('Référence', validators=[DataRequired(), Length(max=50)])
    price = FloatField('Prix unitaire (€)', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Le prix doit être supérieur à 0')
    ])
    quantity = IntegerField('Quantité en stock', validators=[
        DataRequired(),
        NumberRange(min=0, message='La quantité ne peut pas être négative')
    ])
    category = SelectField('Catégorie', choices=[
        ('Électronique', 'Électronique'),
        ('Vêtements', 'Vêtements'),
        ('Alimentation', 'Alimentation'),
        ('Maison', 'Maison'),
        ('Sport', 'Sport'),
        ('Livres', 'Livres'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Enregistrer')
    
    def __init__(self, original_reference=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.original_reference = original_reference
    
    def validate_reference(self, reference):
        if reference.data != self.original_reference:
            product = Product.query.filter_by(reference=reference.data).first()
            if product:
                raise ValidationError('Cette référence est déjà utilisée.')

class SaleForm(FlaskForm):
    product_id = SelectField('Produit', coerce=int, validators=[DataRequired()])
    quantity_sold = IntegerField('Quantité vendue', validators=[
        DataRequired(),
        NumberRange(min=1, message='La quantité doit être supérieure à 0')
    ])
    submit = SubmitField('Enregistrer la vente')
    
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, f'{p.name} (Stock: {p.quantity})') 
                                  for p in Product.query.filter(Product.quantity > 0).all()]

class SearchForm(FlaskForm):
    search_query = StringField('Rechercher un produit', validators=[Length(max=100)])
    category_filter = SelectField('Filtrer par catégorie', choices=[
        ('', 'Toutes les catégories'),
        ('Électronique', 'Électronique'),
        ('Vêtements', 'Vêtements'),
        ('Alimentation', 'Alimentation'),
        ('Maison', 'Maison'),
        ('Sport', 'Sport'),
        ('Livres', 'Livres'),
        ('Autre', 'Autre')
    ])
    submit = SubmitField('Rechercher')
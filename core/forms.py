from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from crispy_forms.bootstrap import FormActions
from .models import *


class CustomUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário customizado"""
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=False)
    endereco = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), required=False, empty_label="Selecione a cidade")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 
                 'telefone', 'endereco', 'cidade', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('user_type', css_class='form-group col-md-6 mb-0'),
                Column('telefone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'endereco',
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Cadastrar', css_class='btn btn-success')
            )
        )


class CustomAuthenticationForm(AuthenticationForm):
    """Formulário de login customizado"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('submit', 'Entrar', css_class='btn btn-success')
            )
        )


class ProdutoForm(forms.ModelForm):
    """Formulário para produtos"""
    
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'preco', 'unidade', 
                 'quantidade_disponivel', 'imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nome',
            Row(
                Column('categoria', css_class='form-group col-md-6 mb-0'),
                Column('preco', css_class='form-group col-md-3 mb-0'),
                Column('unidade', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'quantidade_disponivel',
            'descricao',
            'imagem',
            FormActions(
                Submit('submit', 'Salvar Produto', css_class='btn btn-success')
            )
        )


class CategoriaForm(forms.ModelForm):
    """Formulário para categorias"""
    
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nome',
            'descricao',
            FormActions(
                Submit('submit', 'Salvar Categoria', css_class='btn btn-success')
            )
        )


class PedidoForm(forms.ModelForm):
    """Formulário para pedidos"""
    
    class Meta:
        model = Pedido
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'observacoes',
            FormActions(
                Submit('submit', 'Finalizar Pedido', css_class='btn btn-success')
            )
        )



class BuscaProdutoForm(forms.Form):
    busca = forms.CharField(required=False, label='Buscar produto')
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Categoria'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('busca', css_class='form-group col-md-8 mb-0'),
                Column('categoria', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Buscar', css_class='btn btn-success')  # botão verde sólido
            )
        )


class AtualizaStatusPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Só produtores podem atualizar status
        if user and user.user_type == 'produtor':
            self.fields['status'].choices = [
                ('em_preparacao', 'Em Preparação'),
                ('enviado', 'Enviado'),
                ('concluido', 'Concluído'),
            ]
        else:
            self.fields['status'].choices = []

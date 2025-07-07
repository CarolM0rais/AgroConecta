from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cidade, Produto, Pedido, Pessoa, TipoPessoa

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = ['nome', 'uf']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'preco',
            'unidade_medida',
            'quantidade_disponivel',
            'produtor',
            'categoria',
            'foto',  # Inclui o campo foto para upload
        ]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'forma_pagamento', 'status', 'valor_total']

# Formulário para registrar usuário e pessoa - Cliente
class RegistroClienteForm(UserCreationForm):
    nome = forms.CharField(max_length=150)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nome', 'cidade']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Certifica que o email será salvo
        if commit:
            user.save()
            Pessoa.objects.create(
                user=user,
                nome=self.cleaned_data['nome'],
                tipo=TipoPessoa.CLIENTE,
                cidade=self.cleaned_data.get('cidade'),
            )
        return user

# Formulário para registrar usuário e pessoa - Produtor
class RegistroProdutorForm(UserCreationForm):
    nome = forms.CharField(max_length=150)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nome', 'cidade']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Certifica que o email será salvo
        if commit:
            user.save()
            Pessoa.objects.create(
                user=user,
                nome=self.cleaned_data['nome'],
                tipo=TipoPessoa.PRODUTOR,
                cidade=self.cleaned_data.get('cidade'),
            )
        return user

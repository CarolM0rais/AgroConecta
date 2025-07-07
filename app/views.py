from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import *
from .forms import CidadeForm, ProdutoForm, PedidoForm, RegistroClienteForm, RegistroProdutorForm

# Página inicial
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# Cidades
class CidadeListView(LoginRequiredMixin, View):
    def get(self, request):
        cidades = Cidade.objects.all()
        return render(request, 'cidade.html', {'cidades': cidades})

class CidadeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = CidadeForm()
        return render(request, 'cidade_form.html', {'form': form})

    def post(self, request):
        form = CidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cidade criada com sucesso!')
            return redirect('cidade-list')
        return render(request, 'cidade_form.html', {'form': form})

# Produtos
class ProdutoListView(LoginRequiredMixin, View):
    def get(self, request):
        produtos = Produto.objects.all()
        return render(request, 'produto.html', {'produtos': produtos})

class ProdutoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProdutoForm()
        return render(request, 'produto_form.html', {'form': form})

    def post(self, request):
        form = ProdutoForm(request.POST, request.FILES)  # Importante receber arquivos!
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('lista_produtos')
        return render(request, 'produto_form.html', {'form': form})

# Pedidos
class PedidoListView(LoginRequiredMixin, View):
    def get(self, request):
        pedidos = Pedido.objects.select_related('cliente', 'forma_pagamento').all()
        return render(request, 'pedido.html', {'pedidos': pedidos})

class PedidoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PedidoForm()
        return render(request, 'pedido_form.html', {'form': form})

    def post(self, request):
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido criado com sucesso!')
            return redirect('lista_pedidos')
        return render(request, 'pedido_form.html', {'form': form})

# Listagem de Produtores
@login_required
def lista_produtores(request):
    produtores = Pessoa.objects.filter(tipo=TipoPessoa.PRODUTOR)
    return render(request, 'produtor.html', {'produtores': produtores})

# Listagem de Clientes
@login_required
def lista_clientes(request):
    clientes = Pessoa.objects.filter(tipo=TipoPessoa.CLIENTE)
    return render(request, 'cliente.html', {'clientes': clientes})

# Autenticação
class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class RegistroClienteView(View):
    def get(self, request):
        form = RegistroClienteForm()
        return render(request, 'registro_cliente.html', {'form': form})

    def post(self, request):
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            messages.success(request, 'Registro realizado com sucesso! Bem-vindo(a)!')
            return redirect('index')
        return render(request, 'registro_cliente.html', {'form': form})

class RegistroProdutorView(View):
    def get(self, request):
        form = RegistroProdutorForm()
        return render(request, 'registro_produtor.html', {'form': form})

    def post(self, request):
        form = RegistroProdutorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            messages.success(request, 'Registro realizado com sucesso! Bem-vindo(a)!')
            return redirect('index')
        return render(request, 'registro_produtor.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import *
from .forms import CidadeForm, ProdutoForm, PedidoForm, RegistroClienteForm, RegistroProdutorForm, TipoPessoa

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
        user = request.user
        if user.is_superuser:
            produtos = Produto.objects.all()
        elif hasattr(user, 'pessoa') and user.pessoa.tipo in [TipoPessoa.CLIENTE, TipoPessoa.PRODUTOR]:
            produtos = Produto.objects.all()
        else:
            messages.error(request, 'Você não tem permissão para acessar os produtos.')
            return redirect('index')
        return render(request, 'produto.html', {'produtos': produtos})

class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and hasattr(user, 'pessoa') and user.pessoa.tipo == TipoPessoa.PRODUTOR

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar essa página.")
        return redirect('lista_produtos')

    def get(self, request):
        form = ProdutoForm()
        return render(request, 'produto_form.html', {'form': form})

    def post(self, request):
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.produtor = request.user.pessoa  # Atribui o produtor logado aqui
            produto.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('lista_produtos')
        return render(request, 'produto_form.html', {'form': form})

# Pedidos
class PedidoListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_superuser:
            pedidos = Pedido.objects.select_related('cliente', 'forma_pagamento').all()
        elif hasattr(user, 'pessoa') and user.pessoa.tipo in [TipoPessoa.CLIENTE, TipoPessoa.PRODUTOR]:
            pedidos = Pedido.objects.filter(cliente=user.pessoa).select_related('forma_pagamento')
        else:
            messages.error(request, 'Você não tem permissão para acessar os pedidos.')
            return redirect('index')
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
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
    produtores = Pessoa.objects.filter(tipo=TipoPessoa.PRODUTOR)
    return render(request, 'produtor.html', {'produtores': produtores})

# Listagem de Clientes
@login_required
def lista_clientes(request):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
    clientes = Pessoa.objects.filter(tipo=TipoPessoa.CLIENTE)
    return render(request, 'cliente.html', {'clientes': clientes})

# Autenticação
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'pessoa'):
            tipo = user.pessoa.tipo
            if tipo == TipoPessoa.CLIENTE:
                messages.success(self.request, f'Bem-vindo(a), {user.pessoa.nome} (Cliente)!')
                return reverse_lazy('index')
            elif tipo == TipoPessoa.PRODUTOR:
                messages.success(self.request, f'Bem-vindo(a), {user.pessoa.nome} (Produtor)!')
                return reverse_lazy('lista_produtos')
            elif tipo == TipoPessoa.ADMIN:
                messages.success(self.request, f'Bem-vindo(a), {user.pessoa.nome} (Administrador)!')
                return reverse_lazy('admin:index')
        messages.warning(self.request, 'Seu perfil ainda não está vinculado a um tipo de usuário.')
        return reverse_lazy('index')

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

class ProdutoDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk)
        return render(request, 'produto_detalhe.html', {'produto': produto})

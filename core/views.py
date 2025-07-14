from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from .models import CustomUser, Produto, Categoria, Pedido, ItemPedido
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import (
    CustomUserCreationForm, ProdutoForm, CategoriaForm, 
    PedidoForm, BuscaProdutoForm
)


def home(request):
    """Página inicial"""
    produtos_recentes = Produto.objects.filter(ativo=True)[:6]
    categorias = Categoria.objects.all()[:8]
    
    context = {
        'produtos_recentes': produtos_recentes,
        'categorias': categorias,
    }
    return render(request, 'core/home.html', context)


def register(request):
    """Registro de usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # ou 'produto_list' se preferir


class ProdutoListView(ListView):
    """Lista de produtos"""
    model = Produto
    template_name = 'core/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Produto.objects.filter(ativo=True)
        
        # Busca por texto
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | 
                Q(descricao__icontains=busca)
            )
        
        # Filtro por categoria
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        return queryset.order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BuscaProdutoForm(self.request.GET)
        context['categorias'] = Categoria.objects.all()
        return context


class ProdutoDetailView(DetailView):
    """Detalhes do produto"""
    model = Produto
    template_name = 'core/produto_detail.html'
    context_object_name = 'produto'


@login_required
def produto_create(request):
    """Criar produto (apenas produtores)"""
    if request.user.user_type != 'produtor':
        messages.error(request, 'Apenas produtores podem cadastrar produtos.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.produtor = request.user
            produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    
    return render(request, 'core/produto_form.html', {'form': form})


@login_required
def produto_update(request, pk):
    """Atualizar produto"""
    produto = get_object_or_404(Produto, pk=pk)
    
    if produto.produtor != request.user:
        messages.error(request, 'Você não tem permissão para editar este produto.')
        return redirect('produto_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'core/produto_form.html', {'form': form, 'produto': produto})


@login_required
def produto_delete(request, pk):
    """Deletar produto"""
    produto = get_object_or_404(Produto, pk=pk)
    
    if produto.produtor != request.user:
        messages.error(request, 'Você não tem permissão para deletar este produto.')
        return redirect('produto_detail', pk=pk)
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto deletado com sucesso!')
        return redirect('produto_list')
    
    return render(request, 'core/produto_confirm_delete.html', {'produto': produto})


class CategoriaListView(ListView):
    """Lista de categorias"""
    model = Categoria
    template_name = 'core/categoria_list.html'
    context_object_name = 'categorias'


@login_required
def meus_produtos(request):
    """Produtos do usuário logado"""
    if request.user.user_type != 'produtor':
        messages.error(request, 'Apenas produtores podem acessar esta página.')
        return redirect('home')
    
    produtos = Produto.objects.filter(produtor=request.user).order_by('-data_criacao')
    return render(request, 'core/meus_produtos.html', {'produtos': produtos})


@login_required
def meus_pedidos(request):
    """Pedidos do usuário logado"""
    if request.user.user_type == 'comprador':
        pedidos = Pedido.objects.filter(comprador=request.user).order_by('-data_pedido')
    else:
        # Para produtores, mostrar pedidos dos seus produtos
        pedidos = Pedido.objects.filter(
            itens__produto__produtor=request.user
        ).distinct().order_by('-data_pedido')
    
    return render(request, 'core/meus_pedidos.html', {'pedidos': pedidos})


class PedidoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes do pedido"""
    model = Pedido
    template_name = 'core/pedido_detail.html'
    context_object_name = 'pedido'
    
    def get_queryset(self):
        if self.request.user.user_type == 'comprador':
            return Pedido.objects.filter(comprador=self.request.user)
        else:
            # Para produtores, mostrar apenas pedidos dos seus produtos
            return Pedido.objects.filter(
                itens__produto__produtor=self.request.user
            ).distinct()


@login_required
def adicionar_ao_carrinho(request, produto_id):
    """Adicionar produto ao carrinho (sessão)"""
    if request.user.user_type != 'comprador':
        return JsonResponse({'error': 'Apenas compradores podem adicionar ao carrinho.'})
    
    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    quantidade = int(request.POST.get('quantidade', 1))
    
    # Usar sessão para carrinho
    carrinho = request.session.get('carrinho', {})
    
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]['quantidade'] += quantidade
    else:
        carrinho[str(produto_id)] = {
            'nome': produto.nome,
            'preco': float(produto.preco),
            'quantidade': quantidade,
            'produtor': produto.produtor.username
        }
    
    request.session['carrinho'] = carrinho
    request.session.modified = True
    
    messages.success(request, f'{produto.nome} adicionado ao carrinho!')
    return redirect('produto_detail', pk=produto_id)


@login_required
def carrinho(request):
    """Visualizar carrinho"""
    if request.user.user_type != 'comprador':
        messages.error(request, 'Apenas compradores podem acessar o carrinho.')
        return redirect('home')
    
    carrinho = request.session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    
    return render(request, 'core/carrinho.html', {
        'carrinho': carrinho,
        'total': total
    })


@login_required
def finalizar_pedido(request):
    """Finalizar pedido"""
    if request.user.user_type != 'comprador':
        messages.error(request, 'Apenas compradores podem finalizar pedidos.')
        return redirect('home')
    
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('produto_list')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.comprador = request.user
            pedido.save()
            
            # Criar itens do pedido
            for produto_id, item in carrinho.items():
                produto = get_object_or_404(Produto, pk=produto_id)
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=item['quantidade'],
                    preco_unitario=produto.preco
                )
            
            # Limpar carrinho
            request.session['carrinho'] = {}
            request.session.modified = True
            
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('pedido_detail', pk=pedido.pk)
    else:
        form = PedidoForm()
    
    # Reestruturar o carrinho para incluir total por item
    carrinho_detalhado = []
    total = 0

    for produto_id, item in carrinho.items():
        subtotal = item['preco'] * item['quantidade']
        total += subtotal
        carrinho_detalhado.append({
            'id': produto_id,
            'nome': item.get('nome'),
            'preco': item['preco'],
            'quantidade': item['quantidade'],
            'subtotal': subtotal
        })
    
    return render(request, 'core/finalizar_pedido.html', {
        'form': form,
        'carrinho': carrinho_detalhado,
        'total': total
    })

def custom_404(request, exception):
    """Página de erro 404 customizada"""
    return render(request, 'core/404.html', status=404)


def custom_500(request):
    """Página de erro 500 customizada"""
    return render(request, 'core/500.html', status=500)


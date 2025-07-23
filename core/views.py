from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import CustomUser, Produto, Categoria, Pedido, ItemPedido
from .forms import (
    CustomUserCreationForm, ProdutoForm, CategoriaForm,
    PedidoForm, BuscaProdutoForm, AvaliacaoPedidoForm
)

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# Home
def home(request):
    produtos_recentes = Produto.objects.filter(ativo=True).order_by('-data_criacao')[:6]
    categorias = Categoria.objects.all()[:8]

    context = {
        'produtos_recentes': produtos_recentes,
        'categorias': categorias,
    }
    return render(request, 'core/home.html', context)

# Avaliar pedido
@login_required
def avaliar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, comprador=request.user)

    # Permite avaliação só se pedido entregue
    if pedido.status != 'entregue':
        return redirect('pedido_detail', pk=pedido_id)

    # Evita avaliação duplicada
    if hasattr(pedido, 'avaliacao'):
        return redirect('pedido_detail', pk=pedido_id)

    if request.method == 'POST':
        form = AvaliacaoPedidoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pedido = pedido
            avaliacao.save()
            return redirect('pedido_detail', pk=pedido_id)
    else:
        form = AvaliacaoPedidoForm()

    return render(request, 'core/avaliar_pedido.html', {'form': form, 'pedido': pedido})
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # ou o formulário que você estiver usando

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 9

    def get_queryset(self):
        queryset = Produto.objects.filter(ativo=True).order_by('-data_criacao')
        self.form = BuscaProdutoForm(self.request.GET)

        if self.form.is_valid():
            busca = self.form.cleaned_data.get('busca')
            categoria = self.form.cleaned_data.get('categoria')

            if busca:
                queryset = queryset.filter(
                    Q(nome__icontains=busca) | Q(descricao__icontains=busca)
                )
            if categoria:
                queryset = queryset.filter(categoria=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

# Detalhes do produto
class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'core/produto_detail.html'
    context_object_name = 'produto'

# Criar produto
@login_required
def produto_create(request):
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

# Atualizar produto
@login_required
def produto_update(request, pk):
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

# Deletar produto
@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if produto.produtor != request.user:
        messages.error(request, 'Você não tem permissão para deletar este produto.')
        return redirect('produto_detail', pk=pk)

    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto deletado com sucesso!')
        return redirect('produto_list')

    return render(request, 'core/produto_confirm_delete.html', {'produto': produto})

# Lista de categorias
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'core/categoria_list.html'
    context_object_name = 'categorias'

# Produtos do usuário logado (produtor)
@login_required
def meus_produtos(request):
    if request.user.user_type != 'produtor':
        messages.error(request, 'Apenas produtores podem acessar esta página.')
        return redirect('home')

    produtos = Produto.objects.filter(produtor=request.user).order_by('-data_criacao')
    return render(request, 'core/meus_produtos.html', {'produtos': produtos})

# Pedidos do usuário logado
@login_required
def meus_pedidos(request):
    if request.user.user_type == 'comprador':
        pedidos = Pedido.objects.filter(comprador=request.user).order_by('-data_pedido')
    else:
        pedidos = Pedido.objects.filter(
            itens__produto__produtor=request.user
        ).distinct().order_by('-data_pedido')

    return render(request, 'core/meus_pedidos.html', {'pedidos': pedidos})

# Detalhes do pedido
class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'core/pedido_detail.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        if self.request.user.user_type == 'comprador':
            return Pedido.objects.filter(comprador=self.request.user)
        else:
            return Pedido.objects.filter(
                itens__produto__produtor=self.request.user
            ).distinct()

# Adicionar ao carrinho (sessão)
@login_required
def adicionar_ao_carrinho(request, produto_id):
    if request.user.user_type != 'comprador':
        return JsonResponse({'error': 'Apenas compradores podem adicionar ao carrinho.'})

    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    quantidade = int(request.POST.get('quantidade', 1))

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

# Visualizar carrinho
@login_required
def carrinho(request):
    if request.user.user_type != 'comprador':
        messages.error(request, 'Apenas compradores podem acessar o carrinho.')
        return redirect('home')

    carrinho = request.session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())

    return render(request, 'core/carrinho.html', {
        'carrinho': carrinho,
        'total': total
    })

# Finalizar pedido
@login_required
def finalizar_pedido(request):
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

            for produto_id, item in carrinho.items():
                produto = get_object_or_404(Produto, pk=produto_id)
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=item['quantidade'],
                    preco_unitario=produto.preco
                )

            request.session['carrinho'] = {}
            request.session.modified = True

            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('pedido_detail', pk=pedido.pk)
    else:
        form = PedidoForm()

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

# Atualizar status do pedido (para produtores)
@login_required
def atualizar_status_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    produtores = set(item.produto.produtor for item in pedido.itens.all())
    if request.user not in produtores:
        messages.error(request, "Você não tem permissão para alterar este pedido.")
        return redirect('pedido_detail', pk=pk)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in dict(Pedido.STATUS_CHOICES):
            pedido.status = novo_status
            pedido.save()
            messages.success(request, "Status do pedido atualizado com sucesso.")
        else:
            messages.error(request, "Status inválido.")

    return redirect('pedido_detail', pk=pk)

# Custom error pages
def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

def custom_500(request):
    return render(request, 'core/500.html', status=500)

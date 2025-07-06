from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import *

# Página inicial
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# Listagem e criação de Cidades
class CidadeListView(View):
    def get(self, request):
        cidades = Cidade.objects.all()
        return render(request, 'cidade.html', {'cidades': cidades})

class CidadeCreateView(View):
    def get(self, request):
        return render(request, 'cidade_form.html')

    def post(self, request):
        nome = request.POST.get('nome')
        uf = request.POST.get('uf')

        if not nome or not uf:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'cidade_form.html')

        Cidade.objects.create(nome=nome, uf=uf)
        messages.success(request, 'Cidade criada com sucesso!')
        return redirect('cidade-list')

# Listagem e criação de Produtos
class ProdutoListView(View):
    def get(self, request):
        produtos = Produto.objects.all()  # Removido select_related para evitar problemas com campos nulos
        return render(request, 'produto.html', {'produtos': produtos})


class ProdutoCreateView(View):
    def get(self, request):
        produtores = Pessoa.objects.filter(tipo__nome='produtor')
        categorias = CategoriaProduto.objects.all()
        context = {
            'produtores': produtores,
            'categorias': categorias,
        }
        return render(request, 'produto_form.html', context)

    def post(self, request):
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        unidade_medida = request.POST.get('unidade_medida')
        quantidade_disponivel = request.POST.get('quantidade_disponivel')
        produtor_id = request.POST.get('produtor')
        categoria_id = request.POST.get('categoria')

        # Validação simples
        if not all([nome, preco, unidade_medida, quantidade_disponivel, produtor_id, categoria_id]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            produtores = Pessoa.objects.filter(tipo__nome='produtor')
            categorias = CategoriaProduto.objects.all()
            return render(request, 'produto_form.html', {
                'produtores': produtores,
                'categorias': categorias,
                'nome': nome,
                'descricao': descricao,
                'preco': preco,
                'unidade_medida': unidade_medida,
                'quantidade_disponivel': quantidade_disponivel,
                'produtor_id': produtor_id,
                'categoria_id': categoria_id,
            })

        produtor = get_object_or_404(Pessoa, id=produtor_id)
        categoria = get_object_or_404(CategoriaProduto, id=categoria_id)

        Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            unidade_medida=unidade_medida,
            quantidade_disponivel=quantidade_disponivel,
            produtor=produtor,
            categoria=categoria,
        )

        messages.success(request, 'Produto criado com sucesso!')
        return redirect('lista_produtos')  # Corrigido aqui

# Listagem e criação de Pedidos
class PedidoListView(View):
    def get(self, request):
        pedidos = Pedido.objects.select_related('cliente', 'forma_pagamento').all()
        return render(request, 'pedido.html', {'pedidos': pedidos})

class PedidoCreateView(View):
    def get(self, request):
        clientes = Pessoa.objects.filter(tipo__nome='cliente')
        formas_pagamento = FormaPagamento.objects.all()
        context = {
            'clientes': clientes,
            'formas_pagamento': formas_pagamento,
        }
        return render(request, 'pedido_form.html', context)

    def post(self, request):
        cliente_id = request.POST.get('cliente')
        forma_pagamento_id = request.POST.get('forma_pagamento')
        status = request.POST.get('status', 'pendente')

        if not cliente_id or not forma_pagamento_id:
            messages.error(request, 'Por favor, selecione cliente e forma de pagamento.')
            clientes = Pessoa.objects.filter(tipo__nome='cliente')
            formas_pagamento = FormaPagamento.objects.all()
            return render(request, 'pedido_form.html', {
                'clientes': clientes,
                'formas_pagamento': formas_pagamento,
                'status': status,
            })

        cliente = get_object_or_404(Pessoa, id=cliente_id)
        forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)

        Pedido.objects.create(
            cliente=cliente,
            forma_pagamento=forma_pagamento,
            status=status,
            valor_total=0,  # Ajustar depois com itens
        )

        messages.success(request, 'Pedido criado com sucesso!')
        return redirect('pedido-list')

# Listagem de Produtores

def lista_produtores(request):
    produtores = Pessoa.objects.filter(tipo=TipoPessoa.PRODUTOR)
    return render(request, 'produtor.html', {'produtores': produtores})


# Listagem de Clientes
def lista_clientes(request):
    clientes = Pessoa.objects.filter(tipo=TipoPessoa.CLIENTE)
    return render(request, 'cliente.html', {'clientes': clientes})
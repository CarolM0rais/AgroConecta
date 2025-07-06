from django.contrib import admin
from django.urls import path
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('cidades/', CidadeListView.as_view(), name='cidade-list'),
    path('cidades/novo/', CidadeCreateView.as_view(), name='cidade-create'),
    path('produtos/', ProdutoListView.as_view(), name='lista_produtos'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('clientes/', lista_clientes, name='lista_clientes'),  # precisa implementar view
    path('pedidos/', PedidoListView.as_view(), name='lista_pedidos'),
    path('pedidos/novo/', PedidoCreateView.as_view(), name='pedido-create'),
    path('produtores/', lista_produtores, name='lista_produtores'),
]

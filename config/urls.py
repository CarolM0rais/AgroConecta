from django.contrib import admin
from django.urls import path
from app.views import (
    IndexView,
    CidadeListView,
    CidadeCreateView,
    ProdutoListView,
    ProdutoCreateView,
    PedidoListView,
    PedidoCreateView,
    ProdutorListView,
    ClienteListView,      # precisa criar essa view
    PedidoListView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('cidades/', CidadeListView.as_view(), name='cidade-list'),
    path('cidades/novo/', CidadeCreateView.as_view(), name='cidade-create'),
    path('produtores/', ProdutorListView.as_view(), name='lista_produtores'),
    path('produtos/', ProdutoListView.as_view(), name='lista_produtos'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'),  # precisa implementar view
    path('pedidos/', PedidoListView.as_view(), name='lista_pedidos'),
    path('pedidos/novo/', PedidoCreateView.as_view(), name='pedido-create'),
]

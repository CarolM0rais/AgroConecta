from django.contrib import admin  # Importar o admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (

    IndexView,
    CidadeListView, CidadeCreateView,
    ProdutoListView, ProdutoCreateView,
    PedidoListView, PedidoCreateView,
    lista_clientes, lista_produtores,
    RegistroClienteView, RegistroProdutorView,
    CustomLoginView, CustomLogoutView,
    ProdutoDetailView,  # <-- importe aqui a nova view de detalhe


)

urlpatterns = [
    path('admin/', admin.site.urls),  # Adiciona o admin
    path('', IndexView.as_view(), name='index'),
    path('produtos/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detalhe'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro-cliente/', RegistroClienteView.as_view(), name='registro_cliente'),
    path('registro-produtor/', RegistroProdutorView.as_view(), name='registro_produtor'),
    path('cidades/', CidadeListView.as_view(), name='cidade-list'),
    path('cidades/nova/', CidadeCreateView.as_view(), name='cidade-create'),
    path('produtos/', ProdutoListView.as_view(), name='lista_produtos'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('pedidos/', PedidoListView.as_view(), name='lista_pedidos'),
    path('pedidos/novo/', PedidoCreateView.as_view(), name='pedido-create'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('produtores/', lista_produtores, name='lista_produtores'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
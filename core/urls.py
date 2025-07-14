from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Produtos
    path('produtos/', views.ProdutoListView.as_view(), name='produto_list'),
    path('produto/<int:pk>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('produto/novo/', views.produto_create, name='produto_create'),
    path('produto/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produto/<int:pk>/deletar/', views.produto_delete, name='produto_delete'),
    
    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    
    # Área do usuário
    path('meus-produtos/', views.meus_produtos, name='meus_produtos'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    
    # Carrinho e pedidos
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar-carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_carrinho'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
]


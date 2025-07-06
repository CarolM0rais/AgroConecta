from django.contrib import admin
from .models import Cidade, CategoriaProduto, Pessoa, Produto, FormaPagamento, Pedido, ItemPedido

admin.site.register(Cidade)
admin.site.register(CategoriaProduto)
admin.site.register(Pessoa)
admin.site.register(Produto)
admin.site.register(FormaPagamento)
admin.site.register(Pedido)
admin.site.register(ItemPedido)

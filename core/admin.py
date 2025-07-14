from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Categoria, Produto, Pedido, ItemPedido


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin para usuário customizado"""
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone', 'endereco')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone', 'endereco')
        }),
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para categorias"""
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
    ordering = ('nome',)


class ItemPedidoInline(admin.TabularInline):
    """Inline para itens do pedido"""
    model = ItemPedido
    extra = 0
    readonly_fields = ('preco_unitario',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """Admin para produtos"""
    list_display = ('nome', 'categoria', 'produtor', 'preco', 'quantidade_disponivel', 'ativo', 'data_criacao')
    list_filter = ('categoria', 'ativo', 'data_criacao', 'produtor__user_type')
    search_fields = ('nome', 'descricao', 'produtor__username')
    list_editable = ('ativo', 'preco', 'quantidade_disponivel')
    ordering = ('-data_criacao',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria', 'produtor')
        }),
        ('Preço e Estoque', {
            'fields': ('preco', 'unidade', 'quantidade_disponivel')
        }),
        ('Mídia', {
            'fields': ('imagem',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Admin para pedidos"""
    list_display = ('id', 'comprador', 'status', 'data_pedido', 'get_total')
    list_filter = ('status', 'data_pedido')
    search_fields = ('comprador__username', 'comprador__email')
    list_editable = ('status',)
    ordering = ('-data_pedido',)
    inlines = [ItemPedidoInline]
    
    def get_total(self, obj):
        return f"R$ {obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    """Admin para itens do pedido"""
    list_display = ('pedido', 'produto', 'quantidade', 'preco_unitario', 'get_subtotal')
    list_filter = ('pedido__status', 'produto__categoria')
    search_fields = ('produto__nome', 'pedido__comprador__username')
    
    def get_subtotal(self, obj):
        return f"R$ {obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'


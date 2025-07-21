from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Categoria, Produto, Pedido, ItemPedido, Cidade


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin para usuário customizado"""
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'cidade', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'cidade')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cidade__nome')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone', 'endereco', 'cidade')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone', 'endereco', 'cidade')
        }),
    )


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


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
    list_display = ('id', 'comprador', 'status', 'data_pedido', 'get_total')
    list_filter = ('status', 'data_pedido')
    search_fields = ('comprador__username', 'comprador__email')
    list_editable = ('status',)
    ordering = ('-data_pedido',)
    inlines = [ItemPedidoInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.user_type == 'produtor':
            # Exibir só pedidos relacionados a produtos desse produtor
            return qs.filter(itens__produto__produtor=request.user).distinct()
        else:
            # Outros usuários não veem nada
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        elif request.user.user_type == 'produtor':
            # Permitir editar só o status (ou seja, deixar só status editável)
            return [field.name for field in self.model._meta.fields if field.name != 'status']
        else:
            return self.model._meta.get_fields()

    def save_model(self, request, obj, form, change):
        # Pode adicionar validação para garantir que produtor só escolha status permitido
        if request.user.user_type == 'produtor':
            allowed_status = ['em_preparacao', 'enviado']
            if obj.status not in allowed_status:
                # Força a não permitir status inválido para produtor
                obj.status = Pedido.objects.get(pk=obj.pk).status if obj.pk else 'pendente'
        super().save_model(request, obj, form, change)
    
    def get_total(self, obj):
        return f"R$ {obj.get_total():.2f}"
    get_total.short_description = 'Total'

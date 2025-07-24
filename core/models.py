from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone

class Cidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Cidade')

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('produtor', 'Produtor'),
        ('comprador', 'Comprador'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='comprador',
        verbose_name='Tipo de Usuário'
    )
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')
    endereco = models.TextField(blank=True, null=True, verbose_name='Endereço')
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Cidade'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='produtos',
        verbose_name='Categoria'
    )
    produtor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='produtos',
        limit_choices_to={'user_type': 'produtor'},
        verbose_name='Produtor'
    )
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço (R$)')
    unidade = models.CharField(max_length=20, default='kg', verbose_name='Unidade')
    quantidade_disponivel = models.PositiveIntegerField(verbose_name='Quantidade Disponível')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name='Imagem')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.nome} - {self.produtor.username}"

    def get_absolute_url(self):
        return reverse('produto_detail', kwargs={'pk': self.pk})


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name='Forma de Pagamento')

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('em_preparacao', 'Em Preparação'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    comprador = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='pedidos',
        limit_choices_to={'user_type': 'comprador'},
        verbose_name='Comprador'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name='Data do Pedido')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        verbose_name='Forma de Pagamento'
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']

    def __str__(self):
        return f"Pedido #{self.pk} - {self.comprador.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.itens.all())

    def get_absolute_url(self):
        return reverse('pedido_detail', kwargs={'pk': self.pk})


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Pedido'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name='Produto'
    )
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade')
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço Unitário'
    )

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        unique_together = ['pedido', 'produto']

    def __str__(self):
        return f"{self.produto.nome} - Qtd: {self.quantidade}"

    def get_subtotal(self):
        return self.quantidade * self.preco_unitario


class AvaliacaoPedido(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='avaliacao')
    nota = models.PositiveSmallIntegerField()  # por exemplo, 1 a 5
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)

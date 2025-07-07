from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.uf}"

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class TipoPessoa(models.TextChoices):
    CLIENTE = 'cliente', 'Cliente'
    PRODUTOR = 'produtor', 'Produtor'
    ADMIN = 'admin', 'Administrador'

class Pessoa(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='pessoa',
        null=True,         # Permite nulo temporariamente
        blank=True         # Permite formulário em branco temporariamente
    )
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TipoPessoa.choices)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

@receiver(post_save, sender=User)
def criar_pessoa(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'pessoa'):
        # Não cria automaticamente para evitar criação automática sem dados completos
        pass


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20)
    quantidade_disponivel = models.DecimalField(max_digits=10, decimal_places=2)
    produtor = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)
    
    foto = models.ImageField(upload_to='produtos_fotos/', null=True, blank=True)  # <<< Novo campo
    
    def clean(self):
        if self.produtor.tipo != TipoPessoa.PRODUTOR:
            raise ValidationError("O campo 'produtor' deve estar associado a uma Pessoa do tipo 'produtor'.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('cancelado', 'Cancelado'),
    ]

    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)

    def clean(self):
        if self.cliente.tipo != TipoPessoa.CLIENTE:
            raise ValidationError("O campo 'cliente' deve estar associado a uma Pessoa do tipo 'cliente'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"

    def get_total_item(self):
        return self.quantidade * self.preco_unitario

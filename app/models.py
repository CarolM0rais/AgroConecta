from django.db import models

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)  # Ex: SP, RJ

    def __str__(self):
        return f"{self.nome} - {self.uf}"

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class TipoPessoa(models.Model):
    nome = models.CharField(max_length=50)  # cliente, produtor, admin

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    nome = models.CharField(max_length=150)
    tipo = models.ForeignKey(TipoPessoa, on_delete=models.PROTECT)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20)
    quantidade_disponivel = models.DecimalField(max_digits=10, decimal_places=2)
    produtor = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'tipo__nome': 'produtor'})
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)

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
    cliente = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'tipo__nome': 'cliente'})
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)

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

# Generated by Django 5.2.4 on 2025-07-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_pedido_forma_pagamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='forma_pagamento',
            field=models.CharField(choices=[('boleto', 'Boleto'), ('cartao', 'Cartão de Crédito'), ('pix', 'PIX'), ('dinheiro,', 'DINHEIRO')], default='boleto', max_length=20, verbose_name='Forma de Pagamento'),
        ),
    ]

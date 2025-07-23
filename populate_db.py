#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgroConecta.settings')
django.setup()

from core.models import CustomUser, Categoria, Produto, Cidade

def populate_database():
    print("Populando banco de dados com dados de exemplo...")

    # Criar cidades
    cidades_data = {
        'Monte Belo': None,
        'Muzambinho': None,
    }
    for nome_cidade in cidades_data.keys():
        cidade_obj, created = Cidade.objects.get_or_create(nome=nome_cidade)
        cidades_data[nome_cidade] = cidade_obj
        if created:
            print(f"✓ Cidade {nome_cidade} criada")

    # Criar usuários produtores
    produtores = []

    if not CustomUser.objects.filter(username='joao_produtor').exists():
        joao = CustomUser.objects.create_user(
            username='joao_produtor',
            email='joao@email.com',
            password='123456',
            first_name='João',
            last_name='Silva',
            user_type='produtor',
            telefone='(11) 99999-1111',
            endereco='Fazenda São João, Zona Rural, Muzambinho',
            cidade=cidades_data['Muzambinho']
        )
        produtores.append(joao)
        print("✓ Produtor João Silva criado")

    if not CustomUser.objects.filter(username='maria_produtora').exists():
        maria = CustomUser.objects.create_user(
            username='maria_produtora',
            email='maria@email.com',
            password='123456',
            first_name='Maria',
            last_name='Santos',
            user_type='produtor',
            telefone='(11) 99999-2222',
            endereco='Sítio Boa Vista, Zona Rural, Muzambinho',
            cidade=cidades_data['Muzambinho']
        )
        produtores.append(maria)
        print("✓ Produtora Maria Santos criada")

    # Criar usuário comprador
    if not CustomUser.objects.filter(username='carlos_comprador').exists():
        carlos = CustomUser.objects.create_user(
            username='carlos_comprador',
            email='carlos@email.com',
            password='123456',
            first_name='Carlos',
            last_name='Oliveira',
            user_type='comprador',
            telefone='(11) 99999-3333',
            endereco='Rua das Flores, 123, Centro, Monte Belo',
            cidade=cidades_data['Monte Belo']
        )
        print("✓ Comprador Carlos Oliveira criado")

    # Criar categorias
    categorias_data = [
        {'nome': 'Frutas', 'descricao': 'Frutas frescas e saborosas'},
        {'nome': 'Verduras', 'descricao': 'Verduras folhosas e nutritivas'},
        {'nome': 'Legumes', 'descricao': 'Legumes frescos e variados'},
        {'nome': 'Grãos', 'descricao': 'Grãos e cereais de qualidade'},
        {'nome': 'Temperos', 'descricao': 'Ervas e temperos naturais'},
        {'nome': 'Orgânicos', 'descricao': 'Produtos orgânicos certificados'},
    ]

    categorias = {}
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao']}
        )
        categorias[cat_data['nome']] = categoria
        if created:
            print(f"✓ Categoria {cat_data['nome']} criada")

    # Obter produtores existentes (atualizados)
    joao = CustomUser.objects.get(username='joao_produtor')
    maria = CustomUser.objects.get(username='maria_produtora')

    # Criar produtos
    produtos_data = [
        {
            'nome': 'Tomate Cereja Orgânico',
            'descricao': 'Tomates cereja orgânicos, doces e suculentos. Cultivados sem agrotóxicos em nossa fazenda familiar.',
            'categoria': 'Orgânicos',
            'produtor': joao,
            'preco': 8.50,
            'unidade': 'kg',
            'quantidade_disponivel': 50
        },
        {
            'nome': 'Alface Crespa',
            'descricao': 'Alface crespa fresca, ideal para saladas. Colhida na manhã do mesmo dia da entrega.',
            'categoria': 'Verduras',
            'produtor': maria,
            'preco': 3.00,
            'unidade': 'unidade',
            'quantidade_disponivel': 100
        },
        {
            'nome': 'Cenoura Baby',
            'descricao': 'Cenouras baby doces e crocantes. Perfeitas para lanches saudáveis e pratos gourmet.',
            'categoria': 'Legumes',
            'produtor': joao,
            'preco': 6.00,
            'unidade': 'kg',
            'quantidade_disponivel': 30
        },
        {
            'nome': 'Banana Prata',
            'descricao': 'Bananas prata maduras e doces. Fonte natural de potássio e energia.',
            'categoria': 'Frutas',
            'produtor': maria,
            'preco': 4.50,
            'unidade': 'kg',
            'quantidade_disponivel': 80
        },
        {
            'nome': 'Feijão Preto',
            'descricao': 'Feijão preto de primeira qualidade. Grãos selecionados e livres de impurezas.',
            'categoria': 'Grãos',
            'produtor': joao,
            'preco': 7.00,
            'unidade': 'kg',
            'quantidade_disponivel': 200
        },
        {
            'nome': 'Manjericão Fresco',
            'descricao': 'Manjericão fresco e aromático. Ideal para temperar pratos italianos e saladas.',
            'categoria': 'Temperos',
            'produtor': maria,
            'preco': 2.50,
            'unidade': 'maço',
            'quantidade_disponivel': 25
        },
        {
            'nome': 'Morango Orgânico',
            'descricao': 'Morangos orgânicos doces e perfumados. Cultivados com amor e cuidado especial.',
            'categoria': 'Orgânicos',
            'produtor': joao,
            'preco': 12.00,
            'unidade': 'kg',
            'quantidade_disponivel': 15
        },
        {
            'nome': 'Rúcula',
            'descricao': 'Rúcula fresca com sabor levemente picante. Perfeita para saladas sofisticadas.',
            'categoria': 'Verduras',
            'produtor': maria,
            'preco': 4.00,
            'unidade': 'maço',
            'quantidade_disponivel': 40
        }
    ]

    for produto_data in produtos_data:
        produto, created = Produto.objects.get_or_create(
            nome=produto_data['nome'],
            defaults={
                'descricao': produto_data['descricao'],
                'categoria': categorias[produto_data['categoria']],
                'produtor': produto_data['produtor'],
                'preco': produto_data['preco'],
                'unidade': produto_data['unidade'],
                'quantidade_disponivel': produto_data['quantidade_disponivel']
            }
        )
        if created:
            print(f"✓ Produto {produto_data['nome']} criado")

    print("\n🎉 Banco de dados populado com sucesso!")
    print("\nCredenciais de acesso:")
    print("Produtor 1: joao_produtor / 123456")
    print("Produtor 2: maria_produtora / 123456")
    print("Comprador: carlos_comprador / 123456")

if __name__ == '__main__':
    populate_database()

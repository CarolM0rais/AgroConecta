# AgroConecta

**Plataforma que conecta produtores rurais diretamente aos compradores**

AgroConecta é uma aplicação web Django moderna e responsiva que facilita a conexão entre produtores agrícolas e compradores, promovendo o comércio direto de produtos frescos e de qualidade.

## 🌟 Características Principais

### Design e Interface
- **Layout responsivo e minimalista** com cores verde e branco
- **Bootstrap 5** para garantir compatibilidade mobile e desktop
- **Interface intuitiva** com navegação clara e organizada
- **Animações suaves** e efeitos visuais modernos

### Funcionalidades
- **Autenticação completa** com tipos de usuário (Produtor/Comprador)
- **Catálogo de produtos** com busca e filtros por categoria
- **Sistema de carrinho** para compradores
- **Gestão de pedidos** com diferentes status
- **Painel administrativo** completo
- **Páginas de erro customizadas** (404/500)

### Arquitetura
- **App único** (`core`) contendo todos os models, views, forms e URLs
- **Templates base** com herança para evitar repetição
- **Organização clara** de arquivos estáticos e media
- **Configuração otimizada** para desenvolvimento e produção

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone ou extraia o projeto
```bash
# Se usando Git
git clone <url-do-repositorio>
cd AgroConecta

# Ou extraia o arquivo ZIP e navegue até a pasta
```

### 2. Instale as dependências
```bash
pip install django django-crispy-forms crispy-bootstrap5
```

### 3. Configure o banco de dados
```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser
```

### 4. Popular com dados de exemplo (opcional)
```bash
python populate_db.py
```

### 5. Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### 6. Executar o servidor
```bash
python manage.py runserver
```

O projeto estará disponível em: `http://localhost:8000`

## 👥 Usuários de Teste

Após executar o script `populate_db.py`, você terá acesso aos seguintes usuários:

### Administrador
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Acesso:** Django Admin (`/admin/`)

### Produtores
- **Usuário:** `joao_produtor` | **Senha:** `123456`
- **Usuário:** `maria_produtora` | **Senha:** `123456`

### Comprador
- **Usuário:** `carlos_comprador` | **Senha:** `123456`

## 📁 Estrutura do Projeto

```
AgroConecta/
├── AgroConecta/                 # Configurações do projeto
│   ├── __init__.py
│   ├── settings.py              # Configurações principais
│   ├── urls.py                  # URLs principais
│   └── wsgi.py                  # Configuração WSGI
├── core/                        # App principal (único)
│   ├── migrations/              # Migrações do banco
│   ├── __init__.py
│   ├── admin.py                 # Configuração do admin
│   ├── forms.py                 # Formulários unificados
│   ├── models.py                # Models unificados
│   ├── urls.py                  # URLs unificadas
│   └── views.py                 # Views unificadas
├── templates/                   # Templates HTML
│   ├── base.html                # Template base
│   ├── core/                    # Templates do app core
│   └── registration/            # Templates de autenticação
├── static/                      # Arquivos estáticos
│   ├── css/
│   │   └── style.css            # CSS customizado
│   ├── js/
│   └── images/
├── media/                       # Arquivos de upload
├── staticfiles/                 # Arquivos estáticos coletados
├── manage.py                    # Script de gerenciamento Django
├── populate_db.py               # Script para popular BD
└── README.md                    # Esta documentação
```

## 🎨 Design e Estilo

### Paleta de Cores
- **Verde Principal:** `#198754`
- **Verde Claro:** `#20c997`
- **Verde Escuro:** `#146c43`
- **Branco:** `#ffffff`
- **Cinza Claro:** `#f8f9fa`

### Componentes Visuais
- **Bootstrap 5** como framework CSS base
- **Bootstrap Icons** para ícones consistentes
- **CSS customizado** para personalização específica
- **Animações CSS** para melhor experiência do usuário

## 🔧 Configurações Importantes

### ALLOWED_HOSTS
O projeto está configurado com `ALLOWED_HOSTS = ['*']` para facilitar o desenvolvimento. **Em produção, configure hosts específicos.**

### Arquivos Estáticos
- **STATIC_URL:** `/static/`
- **STATIC_ROOT:** `staticfiles/`
- **MEDIA_URL:** `/media/`
- **MEDIA_ROOT:** `media/`

### Banco de Dados
- **Desenvolvimento:** SQLite (`db.sqlite3`)
- **Produção:** Configure PostgreSQL ou MySQL conforme necessário

## 📱 Funcionalidades por Tipo de Usuário

### Produtores
- ✅ Cadastrar e gerenciar produtos
- ✅ Visualizar pedidos recebidos
- ✅ Atualizar status dos pedidos
- ✅ Controlar estoque
- ✅ Editar informações de produtos

### Compradores
- ✅ Navegar catálogo de produtos
- ✅ Buscar e filtrar produtos
- ✅ Adicionar produtos ao carrinho
- ✅ Finalizar pedidos
- ✅ Acompanhar histórico de pedidos

### Administradores
- ✅ Gerenciar usuários
- ✅ Moderar produtos
- ✅ Acompanhar pedidos
- ✅ Gerenciar categorias
- ✅ Acesso completo ao Django Admin

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.4** - Framework web Python
- **SQLite** - Banco de dados (desenvolvimento)
- **django-crispy-forms** - Estilização de formulários
- **crispy-bootstrap5** - Integração Bootstrap com Crispy Forms

### Frontend
- **Bootstrap 5.3.0** - Framework CSS responsivo
- **Bootstrap Icons** - Biblioteca de ícones
- **CSS3** - Estilização customizada
- **JavaScript** - Interatividade básica

### Ferramentas
- **Python 3.11** - Linguagem de programação
- **pip** - Gerenciador de pacotes
- **Django Admin** - Interface administrativa

## 🔒 Segurança

### Medidas Implementadas
- **CSRF Protection** habilitado
- **Validação de formulários** com Django Forms
- **Autenticação robusta** com Django Auth
- **Controle de permissões** por tipo de usuário
- **Validação de dados** nos models

### Recomendações para Produção
- Configure `DEBUG = False`
- Use `SECRET_KEY` segura e única
- Configure `ALLOWED_HOSTS` específicos
- Use HTTPS
- Configure banco de dados robusto
- Implemente backup regular

## 📈 Melhorias Futuras

### Funcionalidades Planejadas
- Sistema de avaliações e comentários
- Chat direto entre produtor e comprador
- Integração com sistemas de pagamento
- Notificações por email/SMS
- API REST para aplicativo mobile
- Sistema de geolocalização
- Relatórios e analytics

### Otimizações Técnicas
- Cache com Redis
- Otimização de imagens
- CDN para arquivos estáticos
- Testes automatizados
- CI/CD pipeline
- Monitoramento de performance

## 🐛 Solução de Problemas

### Problemas Comuns

**Erro de migração:**
```bash
python manage.py migrate --run-syncdb
```

**Arquivos estáticos não carregam:**
```bash
python manage.py collectstatic --clear
```

**Erro de permissão em arquivos:**
```bash
chmod -R 755 media/
chmod -R 755 static/
```

**Banco corrompido:**
```bash
rm db.sqlite3
python manage.py migrate
python populate_db.py
```

## 📞 Suporte

Para dúvidas, problemas ou sugestões:

1. Verifique a documentação acima
2. Consulte os logs do Django
3. Verifique as configurações do `settings.py`
4. Teste com dados de exemplo usando `populate_db.py`

## 📄 Licença

Este projeto foi desenvolvido como uma solução personalizada seguindo as especificações fornecidas. Todos os direitos reservados.

---

**Desenvolvido com ❤️ usando Django e Bootstrap**

*AgroConecta - Conectando o Campo à Mesa*


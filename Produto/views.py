from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.db import connection
from collections import namedtuple

from django.contrib import messages

from .models import Produto
from .forms import ProdutoForm

def listar_produtos(request):
    with connection.cursor() as cursor:
        # Função SQL que se quer executar (SELECT, INSERT, DELETE, UPDATE, ...)
        # Parâmetros serão passados nos []
        cursor.execute("SELECT * FROM Produto_produto ORDER BY nome", [])
        # resultado = cursor.fetchall()

        # Função que permite acessar os atributos das tuplas da tabela resultante da query
        resultado = namedtuplefetchall(cursor)
    return render(request, 'Produto/listar.html', 
            {'produtos': resultado}
            )

# Class-Based View - ListView
# Executa a mesma funcionalidade da função "listar_produtos"
class Listar_produtos_lv(ListView):
    # Indicar o nome do produto que quer ser listado
    model = Produto
    # Indicar o template que será utilizado
    template_name = "Produto/listar_lv.html"
    # Nome do objeto no template será "object_list"

def detalhes_produto(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Produto_produto WHERE id=%s", [pk])
        resultado_produto = namedtuplefetchall(cursor)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Licitacao_licitacao WHERE id=%s",
                            [resultado_produto[0].licitacao_id])
        resultado_licitacao = namedtuplefetchall(cursor)

    return render(request, 'Produto/detalhes.html', 
            {'produto': resultado_produto[0],
             'licitacao': resultado_licitacao[0]}
            )

# Class-Based View - DetailView
# Executa a mesma funcionalidade da função "detalhes_produto"
class Detalhes_produtos_dv(DetailView):
    # Indicar o nome do produto que quer ser detalhado
    model = Produto
    # Indicar o template que será utilizado
    template_name = "Produto/detalhes_dv.html"
    # Nome do objeto no template será "object"

def adicionar_produtos(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            fornecedor = form.cleaned_data['fornecedor']
            no_item = form.cleaned_data['no_item']
            quantidade_maxima = form.cleaned_data['quantidade_maxima']
            valor_unitario = form.cleaned_data['valor_unitario']
            licitacao = form.cleaned_data['licitacao']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Produto_produto (nome, descricao, fornecedor, "
                                "no_item, quantidade_maxima, valor_unitario, licitacao_id) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                                [nome, descricao, fornecedor, no_item, quantidade_maxima,
                                    valor_unitario, licitacao.id])
                resultado = cursor.fetchall()
            return redirect('produto:listar')
    else:
        form = ProdutoForm()
    return render(request, 'Produto/adicionar.html',
                {'form': form}
                )

# Class-Based View - CreateView
# Executa a mesma funcionalidade da função "adicionar_produto"
class Adicionar_produtos_cv(CreateView):
    # Indicar o nome do produto que quer ser criado
    model = Produto
    # Indicar o template que será utilizado
    template_name = "Produto/adicionar_cv.html"
    fields = ['nome', 'descricao', 'fornecedor', 'quantidade_maxima',
                    'valor_unitario', 'licitacao', 'no_item']
    # Página para redirecionamento
    success_url = reverse_lazy('produto:listar')

    def form_valid(self, form):
        if Produto.objects.filter(nome = form.cleaned_data['nome']):
            messages.add_message(self.request, messages.WARNING,
                                 "Já existe um produto com esse nome.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(Adicionar_produtos_cv, self).form_valid(form)

    # Nome do objeto no template será "form"

def deletar_produto(request, pk):
    if request.method == 'POST':
        # Quero realmente deletar
        # Cliquei no botão 'Confirmar'

        # Encontrar o nome do produto de id = 'pk'
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produto_produto WHERE id=%s", [pk])
            nome_produto = cursor.fetchall()[0][1]

        # Procura elementos de pedidos que possuam o produto em questão (id=pk)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Pedido_elementos WHERE produto_id=%s", [pk])
            resultado = cursor.fetchall()

        # Se o tamanho desta lista for 0, não foram encontrados pedidos com este produto.
        # Pode deletar
        if len(resultado) == 0:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Produto_produto WHERE id=%s", [pk])
            messages.add_message(request, messages.ERROR, 'Produto ' + nome_produto + ' deletado com sucesso.')
            return redirect('produto:listar')
        
        # Se o ramanho desta lista for > 0, foram encontrados pedidos com este produto.
        # Não pode deletar
        else:
            messages.add_message(request, messages.ERROR, 'Não é possível deletar o produto ' + nome_produto + '. Há pedido associados a este produto.')
            return redirect('produto:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produto_produto WHERE id=%s", [pk])
            resultado = namedtuplefetchall(cursor)
        return render(request, "produto/confirmar_deletar.html", {'produto': resultado[0]})

# Class-Based View - DeleteView
# Executa a mesma funcionalidade da função "deletar_produto"
class Deletar_produtos_dv(DeleteView):
    # Indicar o nome do produto que quer ser deletado
    model = Produto
    # Indicar o template que será utilizado
    template_name = "Produto/confirmar_deletar_dv.html"
    # Página para redirecionamento
    success_url = reverse_lazy('produto:listar')

    # Nome do objeto no template será "object"

def editar_produto(request, pk):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            fornecedor = form.cleaned_data['fornecedor']
            no_item = form.cleaned_data['no_item']
            quantidade_maxima = form.cleaned_data['quantidade_maxima']
            valor_unitario = form.cleaned_data['valor_unitario']
            licitacao = form.cleaned_data['licitacao']

            with connection.cursor() as cursor:
                cursor.execute("UPDATE Produto_produto SET nome=%s, descricao=%s, "
                                "fornecedor=%s, no_item=%s, quantidade_maxima=%s, "
                                "valor_unitario=%s, licitacao_id=%s "
                                "WHERE id=%s", 
                                [nome, descricao, fornecedor, no_item, quantidade_maxima,
                                    valor_unitario, licitacao.id, pk])
                resultado = cursor.fetchall()
            return redirect('produto:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produto_produto WHERE id=%s", [pk])
            resultado_produto = namedtuplefetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Licitacao_licitacao WHERE id=%s", [resultado_produto[0].licitacao_id])
            resultado_licitacao = namedtuplefetchall(cursor)
        form = ProdutoForm(initial={'nome': resultado_produto[0].nome,
                                    'descricao': resultado_produto[0].descricao,
                                    'fornecedor': resultado_produto[0].fornecedor,
                                    'quantidade_maxima': resultado_produto[0].quantidade_maxima,
                                    'valor_unitario': resultado_produto[0].valor_unitario,
                                    'no_item': resultado_produto[0].no_item,
                                    'licitacao': resultado_licitacao[0]
                                    })
    return render(request, 'Produto/editar.html',
                {'form': form}
                )

# Class-Based View - UpdateView
# Executa a mesma funcionalidade da função "deletar_produto"
class Editar_produtos_uv(UpdateView):
    # Indicar o nome do produto que quer ser editado
    model = Produto
    fields = ['nome', 'descricao', 'fornecedor', 'quantidade_maxima',
                    'valor_unitario', 'licitacao', 'no_item']
    # Indicar o template que será utilizado
    template_name = "Produto/editar_uv.html"
    # Página para redirecionamento
    success_url = reverse_lazy('produto:listar')

    # Nome do objeto no template será "form"

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]



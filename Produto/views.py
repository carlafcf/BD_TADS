from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.db import connection
from collections import namedtuple

from .models import Produto
from .forms import ProdutoForm

def listar_produtos(request):
    with connection.cursor() as cursor:
        # Função SQL que se quer executar (SELECT, INSERT, DELETE, UPDATE, ...)
        # Parâmetros serão passados nos []
        cursor.execute("SELECT * FROM Produto_produto", [])
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

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]



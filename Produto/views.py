from django.shortcuts import render
from django.views.generic import ListView

from django.db import connection
from collections import namedtuple

from .models import Produto

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

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]



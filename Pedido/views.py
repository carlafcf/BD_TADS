from django.shortcuts import render

from django.db import connection
from collections import namedtuple

from datetime import date
from django.contrib import messages

def novo_pedido(request):
    if request.method == 'POST':
        lista_id = request.POST.getlist('ids')
        lista_quantidade = request.POST.getlist('quantidades')
        if (len(lista_id) > 0):
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Pedido_pedido (data, status) VALUES (%s, %s)", [date.today(), '1'])
                cursor.execute("SELECT id FROM Pedido_pedido ORDER BY id DESC LIMIT 1", [])
                id_pedido = cursor.fetchone()[0]

                for i in range(len(lista_id)):
                    cursor.execute("INSERT INTO Pedido_elementos (produto_id, pedido_id, quantidade) VALUES (%s, %s, %s)",
                                    [lista_id[i], id_pedido, lista_quantidade[i]])
        else:
            messages.add_message(request, messages.ERROR, 'Não foram adicionados produtos a este pedido.')
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id, p.nome, p.fornecedor, p.valor_unitario, l.orgao, l.no_arp, p.no_item "
                        "FROM Produto_produto p, Licitacao_licitacao l "
                        "WHERE p.licitacao_id = l.id ORDER BY p.nome", [])
        resultado_query = namedtuplefetchall(cursor)
    return render(request, 'pedido/novo.html', {'produtos': resultado_query})

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
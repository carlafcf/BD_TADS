from django.db import models
from datetime import date

from Produto.models import Produto

TIPOS_STATUS = [
    ('1', 'Em espera'),
    ('2', 'Cadastrado'),
    ('3', 'Em análise'),
    ('4', 'Esperando chegar'),
    ('5', 'Finalizado')
]

class Pedido(models.Model):
    data = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=TIPOS_STATUS, default='1')
    produtos = models.ManyToManyField(Produto, through='Elementos')
    # usuario

    def __str__(self):
        return str(self.data)
        # Adicionar representação do usuário
    
    class Meta:
        ordering = ['data', 'status']

class Elementos(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

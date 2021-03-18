from django.db import models
from datetime import date

from Licitacao.models import Licitacao

class Produto(models.Model):
    nome = models.CharField(max_length=300, null=False)
    descricao = models.TextField()
    fornecedor = models.CharField(max_length=300, null=False)
    quantidade_maxima = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    no_item = models.PositiveIntegerField(default=0)
    licitacao = models.ForeignKey(Licitacao, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome + " - " + self.fornecedor
    
    class Meta:
        ordering = ['nome']

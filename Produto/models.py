from django.db import models
from datetime import date

class Produto(models.Model):
    nome = models.CharField(max_length=300, null=False)
    descricao = models.TextField()
    fornecedor = models.CharField(max_length=300, null=False)
    data_validade = models.DateField(default=date.today)
    quantidade_maxima = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # licitacao - foreign key

    def __str__(self):
        return self.nome + " - " + self.fornecedor
    
    class Meta:
        ordering = ['nome']

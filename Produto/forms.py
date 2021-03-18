from django import forms

from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'fornecedor', 'quantidade_maxima',
                    'valor_unitario', 'licitacao', 'no_item']
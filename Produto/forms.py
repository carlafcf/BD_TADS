from django import forms
from django.db import connection

from django.core.exceptions import ValidationError

from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'fornecedor', 'quantidade_maxima',
                    'valor_unitario', 'licitacao', 'no_item']
    
    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome = cleaned_data.get("nome") 

        # Seleciona se há produtos com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produto_produto WHERE nome=%s", [nome])
            resultado_produto = cursor.fetchall()
        
        # Se a lista não foi vazia, há produto com o mesmo nome
        if (len(resultado_produto) != 0):
            raise ValidationError("Já foi criado um produto com este nome. Escolha outro nome.")

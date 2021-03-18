from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path('listar/', views.listar_produtos, name='listar'),
    path('listar_lv/', views.Listar_produtos_lv.as_view(), name='listar_lv'),
    path('detalhes/<int:pk>', views.detalhes_produto, name="detalhes"),
    path('detalhes_dv/<int:pk>/', views.Detalhes_produtos_dv.as_view(), name='detalhes_dv'),
    path('adicionar/', views.adicionar_produtos, name='adicionar'),
]

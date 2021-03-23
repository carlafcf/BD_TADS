from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path('listar/', views.listar_produtos, name='listar'),
    path('listar_lv/', views.Listar_produtos_lv.as_view(), name='listar_lv'),
    path('detalhes/<int:pk>', views.detalhes_produto, name="detalhes"),
    path('detalhes_dv/<int:pk>/', views.Detalhes_produtos_dv.as_view(), name='detalhes_dv'),
    path('adicionar/', views.adicionar_produtos, name='adicionar'),
    path('adicionar_cv/', views.Adicionar_produtos_cv.as_view(), name='adicionar_cv'),
    path('deletar/<int:pk>/', views.deletar_produto, name="deletar"),
    path('deletar_dv/<int:pk>/', views.Deletar_produtos_dv.as_view(), name="deletar_dv"),
    path('editar/<int:pk>', views.editar_produto, name="editar"),
    path('editar_uv/<int:pk>', views.Editar_produtos_uv.as_view(), name="editar_uv"),
]
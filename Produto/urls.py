from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path('listar/', views.listar_produtos, name='listar'),
    path('listar_lv/', views.Listar_produtos_lv.as_view(), name='listar_lv'),
    # path('adicionar/', views.adicionar_produtos, name='adicionar'),
]

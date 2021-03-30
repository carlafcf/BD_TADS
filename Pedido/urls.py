from django.urls import path

from . import views

app_name = "pedido"

urlpatterns = [
    path('novo/', views.novo_pedido, name='novo'),
]
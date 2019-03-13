from django.urls import path, include
from .views import ListaMovimentacoesView


urlpatterns = [
	path('lista/', ListaMovimentacoesView.as_view(), name='planilha-lista')
]

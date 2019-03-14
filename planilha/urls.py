from django.urls import path, include
from .views import ListaMovimentacoesView, AutenticacaoView, FormularioView


urlpatterns = [
	path('lista/', ListaMovimentacoesView.as_view(), name='planilha-lista'),
	path('autenticacao/', AutenticacaoView.as_view(), name='planilha-autenticacao'),
	path('formulario/', FormularioView.as_view(), name='planilha-formulario')
]

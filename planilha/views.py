from rest_framework import generics
from .models import Movimentacao
from .serializers import MovimentacaoSerializer


class ListaMovimentacoesView(generics.ListAPIView):
	serializer_class = MovimentacaoSerializer

	# Retorna apenas as movimentações do usuário logado
	def get_queryset(self):
		q_set = Movimentacao.objects.filter(usuario=self.request.user)
		return q_set

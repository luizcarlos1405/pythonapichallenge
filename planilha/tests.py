from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .serializers import MovimentacaoSerializer
from django.contrib.auth.models import User
from .models import Movimentacao


# Classe base para testar rota lista/
class TesteListaViewBase(APITestCase):

	@staticmethod
	def cria_movimentacao(nome, valor, usuario):
		if not (nome is None and valor is None):
			Movimentacao.objects.create(nome=nome, valor=valor, usuario=usuario)

	def setUp(self):
		# Usuários de teste
		self.usuario1 = User.objects.create(username='teste1', password='senha')
		self.usuario2 = User.objects.create(username='teste2', password='senha')

		# Cria dados para teste
		self.cria_movimentacao("Dividendo Tesla", 15204.23, self.usuario1)
		self.cria_movimentacao("Iof Xiaomi Mi 7", -17.03, self.usuario1)
		self.cria_movimentacao("Achei Na Rua", 5.00, self.usuario2)
		self.cria_movimentacao("Salgado Cantina da Faculdade", 5.00, self.usuario2)


class PegaMovimentacoesTeste(TesteListaViewBase):

	def teste_pega_movimentacoes_usuario1(self):
		"""
		Esse teste garante que apenas todas as movimentações e apenas as Movimentações
		do usuario1 são fornecidas quando o usuario1 está autenticado e faz uma
		requisição GET na rota lista/
		"""
		# Autenticação
		self.client.force_authenticate(self.usuario1)

		# Faz a requisição
		resposta = self.client.get(
			reverse('planilha-lista')
		)

		# Compara a resposta com o banco de dados
		esperado = Movimentacao.objects.filter(usuario=self.usuario1)
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertEqual(resposta.data, serializado.data)
		self.assertEqual(resposta.status_code, status.HTTP_200_OK)

	def teste_pega_movimentacoes_usuario2(self):
		"""
		Esse teste garante que apenas todas as movimentações e apenas as Movimentações
		do usuario1 são fornecidas quando o usuario2 está autenticado e faz uma
		requisição GET na rota lista/
		"""
		# Autenticação
		self.client.force_authenticate(self.usuario2)

		# Faz a requisição
		resposta = self.client.get(
			reverse('planilha-lista')
		)

		# Compara a resposta com o banco de dados
		esperado = Movimentacao.objects.filter(usuario=self.usuario2)
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertEqual(resposta.data, serializado.data)
		self.assertEqual(resposta.status_code, status.HTTP_200_OK)

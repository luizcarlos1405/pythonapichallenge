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
		self.usuario1 = User.objects.create_user(username='teste1', password='senha')
		self.usuario2 = User.objects.create_user(username='teste2', password='senha')

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


# Classe para testar rota autenticacao/
class TesteAutenticacaoView(APITestCase):

	def setUp(self):
		self.usuario = User.objects.create_user(username='teste', password='senha')

	def teste_autenticacao(self):
		"""
		Garante que é possível autenticar a sessão via requisição POST à rota autenticacao/. Também testa se uma requisição GET em lista/ antes de autenticar é proibida.
		"""
		# Antes de autenticar
		resposta_lista = self.client.get(
			reverse('planilha-lista')
		)

		self.assertEqual(resposta_lista.status_code, status.HTTP_403_FORBIDDEN)

		# Autenticação
		resposta_autenticacao = self.client.post(
			reverse('planilha-autenticacao'),
			{'username':'teste', 'password':'senha'}
		)

		# Django LoginView redireciona após o login, fazendo o status retornar 302
		self.assertEqual(resposta_autenticacao.status_code, status.HTTP_302_FOUND)

		# Após autenticar
		resposta_lista = self.client.get(
			reverse('planilha-lista')
		)

		self.assertEqual(resposta_lista.status_code, status.HTTP_200_OK)


# Classe para testar a rota formulario/
class TesteFormularioView(APITestCase):

	def setUp(self):
		self.usuario = User.objects.create_user(username='teste', password='senha')

	def teste_adiciona_banco(self):
		"""
		Garante que é possível adicionar novas movimentações através de uma requisição
		POST na rota formulario/. Também testa a necessidade de autenticação.
		"""
		# Antes de autenticar
		resposta_formulario = self.client.post(
			reverse('planilha-formulario'),
			{'nome': 'Venda do Violão', 'valor': 260.00, 'tipo':'entrada'}
		)

		# A view é protegida com LoginRequiredMixin, portanto a requisição causa
		# o redirecionamento para a página de login autenticacao/.
		self.assertEqual(resposta_formulario.status_code, status.HTTP_302_FOUND)

		resposta_formulario = self.client.post(
			reverse('planilha-formulario'),
			{'nome': 'Amortecedor Dianteiro Esquerdo', 'valor': 465.95, 'tipo':'saida'}
		)

		self.assertEqual(resposta_formulario.status_code, status.HTTP_302_FOUND)
		# Garante que não há nada no banco
		self.assertQuerysetEqual(Movimentacao.objects.all(), [])

		# Autenticação
		resposta_autenticacao = self.client.post(
			reverse('planilha-autenticacao'),
			{'username':'teste', 'password':'senha'}
		)

		# Django LoginView redireciona após o login, fazendo o status retornar 302
		self.assertEqual(resposta_autenticacao.status_code, status.HTTP_302_FOUND)

		# Após autenticar
		# Adiciona 2 movimentações ao banco
		resposta_formulario = self.client.post(
			reverse('planilha-formulario'),
			{'nome': 'Venda do Violão', 'valor': 180.00, 'tipo':'entrada'}
		)

		self.assertEqual(resposta_formulario.status_code, status.HTTP_302_FOUND)

		resposta_formulario = self.client.post(
			reverse('planilha-formulario'),
			{'nome': 'Amortecedor Dianteiro Esquerdo', 'valor': 420.95, 'tipo': 'saida'}
		)

		self.assertEqual(resposta_formulario.status_code, status.HTTP_302_FOUND)

		resposta_lista = self.client.get(
			reverse('planilha-lista')
		)

		# Garante que o banco possui os dois valores adicionados
		self.assertEqual(len(resposta_lista.data), 2)

		# Compara banco com resultado da lista/
		esperado = Movimentacao.objects.filter(usuario=self.usuario)
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertEqual(resposta_lista.data, serializado.data)
		self.assertEqual(resposta_lista.status_code, status.HTTP_200_OK)

		# Testa se o valor marcado como saido é negativo e, o como entrada, positivo
		self.assertGreater(float(serializado.data[0]['valor']), 0)
		self.assertLess(float(serializado.data[1]['valor']), 0)

	def teste_campos_invalidos(self):
		# Autenticação
		self.client.post(
			reverse('planilha-autenticacao'),
			{'username':'teste', 'password':'senha'}
		)

		# Tentantivas
		self.client.post( # Sem especificar se é entrada ou saída
			reverse('planilha-formulario'),
			{'nome': 'Invalido sem tipo definido.', 'valor': 420.95}
		)
		self.client.post( # Sem especificar nome
			reverse('planilha-formulario'),
			{'valor': 420.95, 'tipo':'entrada'}
		)
		self.client.post( # Espeficiando um tipo invalido
			reverse('planilha-formulario'),
			{'nome': 'Invalido menor que zero.', 'valor': -420.95, 'tipo':'invalido'}
		)
		self.client.post( # Tentativa válida para controle
			reverse('planilha-formulario'),
			{'nome': 'Válido.', 'valor': 420.95, 'tipo':'saida'}
		)

		esperado = Movimentacao.objects.filter(usuario=self.usuario)
		serializado = MovimentacaoSerializer(esperado, many=True)

		# O banco deve possuir apenas 1 valor
		self.assertEqual(len(serializado.data), 1)


# Teste para implementar a funcionalidade de ordenação na rota lista/.
class TesteOrdenacao(TesteListaViewBase):

	def teste_ordenacao(self):
		self.cria_movimentacao("Zebra de presente.", 5000.00, self.usuario1)
		self.cria_movimentacao("Tacos de golfe.", 278.90, self.usuario1)

		# Autenticação
		self.client.force_authenticate(self.usuario1)

		# Nome ascendente
		resposta = self.client.get(
			reverse('planilha-lista'),
			{'ordering': 'nome'}
		)

		esperado = Movimentacao.objects.filter(usuario=self.usuario1)
		esperado = esperado.order_by('nome')
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertListEqual(resposta.data, serializado.data)

		# Nome descendente
		resposta = self.client.get(
			reverse('planilha-lista'),
			{'ordering': '-nome'}
		)

		esperado = Movimentacao.objects.filter(usuario=self.usuario1)
		esperado = esperado.order_by('-nome')
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertListEqual(resposta.data, serializado.data)

		# Valor ascendente
		resposta = self.client.get(
			reverse('planilha-lista'),
			{'ordering': 'valor'}
		)

		esperado = Movimentacao.objects.filter(usuario=self.usuario1)
		esperado = esperado.order_by('valor')
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertListEqual(resposta.data, serializado.data)

		# Valor descendente
		resposta = self.client.get(
			reverse('planilha-lista'),
			{'ordering': '-valor'}
		)

		esperado = Movimentacao.objects.filter(usuario=self.usuario1)
		esperado = esperado.order_by('-valor')
		serializado = MovimentacaoSerializer(esperado, many=True)

		self.assertListEqual(resposta.data, serializado.data)

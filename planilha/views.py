from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django import forms
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Movimentacao
from .serializers import MovimentacaoSerializer

class ListaMovimentacoesView(generics.ListAPIView):
	serializer_class = MovimentacaoSerializer

	# Retorna apenas as movimentações do usuário logado
	def get_queryset(self):
		q_set = Movimentacao.objects.filter(usuario=self.request.user)
		return q_set


class AutenticacaoView(LoginView):
	template_name = 'planilha/autenticacao.html'


class MovimentacaoForm(forms.ModelForm):
	ESCOLHAS = (
		('', ''),
		('entrada', 'Entrada'),
		('saida', 'Saída'),
	)
	tipo = forms.ChoiceField(choices=ESCOLHAS, required=True)

	class Meta:
		model = Movimentacao
		fields = ('nome', 'valor', 'tipo')

	def clean(self):
		dados = self.cleaned_data

		if dados.get('valor') < 0:
			self.add_error('valor', 'O valor da movimentação deve ser maior que zero.')

		elif dados.get('tipo') == 'saida':
			self.cleaned_data['valor'] *= -1

		return super(MovimentacaoForm, self).clean()


class FormularioView(LoginRequiredMixin, CreateView):
	form_class = MovimentacaoForm
	template_name = 'planilha/formulario.html'

	def form_valid(self, form):
		form.instance.usuario = self.request.user
		return super().form_valid(form)

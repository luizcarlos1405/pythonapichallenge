from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Movimentacao(models.Model):
	nome = models.CharField(max_length = 100)
	valor = models.DecimalField(decimal_places = 2, max_digits = 15)
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Movimentação'
		verbose_name_plural = 'Movimentações'

	def get_absolute_url(self):
		return reverse('planilha-lista')

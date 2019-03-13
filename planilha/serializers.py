from rest_framework import serializers
from .models import Movimentacao


class MovimentacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movimentacao
		fields = ('nome', 'valor')

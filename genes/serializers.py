from rest_framework import serializers
from .models import Gene

class GeneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ['symbol', 'name', 'alias_symbol', 'gene_group']
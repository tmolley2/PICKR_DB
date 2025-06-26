from rest_framework import serializers
from .models import PrimerPair

class PrimerPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimerPair
        fields = '__all__'

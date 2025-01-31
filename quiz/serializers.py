from rest_framework import serializers
from .models import Scenario, Stat


class ScenarioSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)   
    class Meta:
        model = Scenario
        fields = '__all__'
class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'id_user', 'nbre_questions', 'nbCorrect', 'nbFausse', 'score', 'pourcentage', 'date_test']
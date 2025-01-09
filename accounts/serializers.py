from rest_framework import serializers
from accounts.models import User, Treatment


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ["id", "nome"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "bebe",
            "fuma",
            "diagnostico",
            "diabetes",
            "peso",
            "altura",
            "doencas",
            "tratamentos",
        ]

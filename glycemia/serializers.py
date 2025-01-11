from rest_framework import serializers

from glycemia.models import GlycemiaLog


class GlycemiaLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlycemiaLog
        fields = "__all__"

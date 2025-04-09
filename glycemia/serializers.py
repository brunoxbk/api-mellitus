from django.utils import timezone
from rest_framework import serializers

from glycemia.models import GlycemiaLog


class GlycemiaLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlycemiaLog
        fields = "__all__"

    # def validate(self, attrs):

    #     user = self.context.get("request").user

    #     date_only = timezone.now().date()

    #     if GlycemiaLog.objects.filter(
    #         user=user, measurement_time__date=date_only
    #     ).exists():
    #         print("existe")
    #         raise serializers.ValidationError(
    #             "Já existe uma medição registrada para este usuário neste dia."
    #         )

    #     return super().validate(attrs)

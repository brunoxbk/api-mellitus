from rest_framework import generics

from glycemia.models import GlycemiaLog
from glycemia.serializers import GlycemiaLogSerializer


class GlycemiaLogListCreateView(generics.ListCreateAPIView):
    queryset = GlycemiaLog.objects.all()
    serializer_class = GlycemiaLogSerializer


class GlycemiaLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GlycemiaLog.objects.all()
    serializer_class = GlycemiaLogSerializer

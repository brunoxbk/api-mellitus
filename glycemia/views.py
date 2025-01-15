from rest_framework import generics

from glycemia.models import GlycemiaLog
from glycemia.serializers import GlycemiaLogSerializer


class GlycemiaLogListCreateView(generics.ListCreateAPIView):
    queryset = GlycemiaLog.objects.all()
    serializer_class = GlycemiaLogSerializer

    def get_queryset(self):
        return GlycemiaLog.objects.filter(user=self.request.user)


class GlycemiaLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GlycemiaLog.objects.all()
    serializer_class = GlycemiaLogSerializer

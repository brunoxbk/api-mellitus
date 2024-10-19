from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, Treatment
from accounts.serializers import UserSerializer,  TreatmentSerializer


class TreatmentListView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
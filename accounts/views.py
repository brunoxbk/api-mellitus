from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserUpdateSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
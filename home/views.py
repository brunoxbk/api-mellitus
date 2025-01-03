from django.http import JsonResponse
from rest_framework import viewsets
from .models import Category, PostPage
from .serializers import CategorySerializer, PostPageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class HomeView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        return Response({"status": "ok"})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostPage.objects.all()
    serializer_class = PostPageSerializer

    def list(self, request):
        queryset = self.queryset

        if request.GET.get("category", None):
            category = request.GET["category"]
            queryset = self.queryset.filter(categories=category)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


def home(request):
    data = {"ok": "ok"}
    return JsonResponse(data)

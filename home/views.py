from django.http import JsonResponse
from rest_framework import viewsets
from .models import Category, PostPage
from .serializers import CategorySerializer, PostPageSerializer, PageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from wagtail.models import Page, Site
from rest_framework import permissions
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


class HomeView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        return Response({"status": "ok"})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(never_cache, name='dispatch')
class PostPageViewSet(viewsets.ModelViewSet):
    queryset = PostPage.objects.live()
    serializer_class = PostPageSerializer

    def list(self, request):
        queryset = PostPage.objects.live()
        if request.GET.get("category", None):
            category = request.GET["category"]
            queryset = self.queryset.filter(categories=category)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PageTreeAPIView(APIView):
    serializer_class = PageSerializer
    
    def get_queryset(self):
        # Obtém a página raiz
        root_page = Page.objects.filter(depth=1).first()
        if not root_page:
            return Page.objects.none()
        
        root_id = self.request.GET.get('root_id', None)
        if root_id and root_id.isdigit():
            custom_root = Page.objects.filter(id=int(root_id)).first()
            if custom_root:
                root_page = custom_root
        
        # Retorna a página raiz (que incluirá os filhos recursivamente)
        return Page.objects.filter(id=root_page.id)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Nenhuma página raiz encontrada"})
        
        root_page = queryset.first()
        serializer = self.serializer_class(root_page)
        return Response(serializer.data)


def home(request):
    data = {"ok": "ok"}
    return JsonResponse(data)

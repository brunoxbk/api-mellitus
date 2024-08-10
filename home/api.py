from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from home.views import CategoryViewSet, PostPageViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
api_router = WagtailAPIRouter('wagtailapi')


router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'postpages', PostPageViewSet, basename='postpages')
api_router.register_endpoint('pages', PagesAPIViewSet)
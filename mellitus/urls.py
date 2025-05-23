from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from home.views import HomeView, PageTreeAPIView
from search import views as search_views
from home.api import api_router, router

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v2/", api_router.urls),
    path("api/v2/", include(router.urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/", include("accounts.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/instruments/", include("instruments.urls")),
    path("api/medications/", include("medications.urls")),
    path("api/glycemia-logs/", include("glycemia.urls")),
    path("api/todo/", include("todo.urls")),
    path("api/page-tree/", PageTreeAPIView.as_view(), name='page-tree'),
    path("", include(wagtail_urls)),
    path("", HomeView.as_view(), name="home"),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

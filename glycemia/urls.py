from django.urls import path

from glycemia.views import GlycemiaLogDetailView, GlycemiaLogListCreateView

urlpatterns = [
    path(
        "",
        GlycemiaLogListCreateView.as_view(),
        name="glycemia-log-list-create",
    ),
    path(
        "<int:pk>/",
        GlycemiaLogDetailView.as_view(),
        name="glycemia-log-detail",
    ),
]

from django.urls import path

from glycemia.views import GlycemiaLogDetailView, GlycemiaLogListCreateView

urlpatterns = [
    path(
        "glycemia-logs/",
        GlycemiaLogListCreateView.as_view(),
        name="glycemia-log-list-create",
    ),
    path(
        "glycemia-logs/<int:pk>/",
        GlycemiaLogDetailView.as_view(),
        name="glycemia-log-detail",
    ),
]

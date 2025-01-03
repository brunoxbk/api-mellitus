from django.urls import path
from .views import (
    MedicationListCreateView,
    MedicationDetailView,
    MedicationLogListCreateView,
    MedicationLogDetailView,
)

urlpatterns = [
    path(
        "",
        MedicationListCreateView.as_view(),
        name="medication-list-create",
    ),
    path(
        "<int:pk>/",
        MedicationDetailView.as_view(),
        name="medication-detail",
    ),
    path(
        "logs/",
        MedicationLogListCreateView.as_view(),
        name="medicationlog-list-create",
    ),
    path(
        "logs/<int:pk>/",
        MedicationLogDetailView.as_view(),
        name="medicationlog-detail",
    ),
]

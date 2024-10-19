from django.urls import path
from accounts.views import UserUpdateView, TreatmentListView

urlpatterns = [
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('treatments/', TreatmentListView.as_view(), name='treatment-list'),
]
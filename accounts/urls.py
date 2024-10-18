from django.urls import path
from .views import UserUpdateView

urlpatterns = [
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
]
from django.urls import path
from .views import (
    FormListCreateView, FormDetailView, 
    QuestionListCreateView, QuestionDetailView, 
    ChoiceListCreateView, ChoiceDetailView, 
    AnswerSheetListCreateView, AnswerSheetDetailView,
    AnswerListCreateView, AnswerDetailView
)

urlpatterns = [
    path('forms/', FormListCreateView.as_view(), name='form-list-create'),
    path('forms/<int:pk>/', FormDetailView.as_view(), name='form-detail'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('choices/', ChoiceListCreateView.as_view(), name='choice-list-create'),
    path('choices/<int:pk>/', ChoiceDetailView.as_view(), name='choice-detail'),
    path('answer-sheets/', AnswerSheetListCreateView.as_view(), name='answer-sheet-list-create'),
    path('answer-sheets/<int:pk>/', AnswerSheetDetailView.as_view(), name='answer-sheet-detail'),
    path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
]
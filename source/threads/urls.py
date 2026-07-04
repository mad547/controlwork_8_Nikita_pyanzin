from django.urls import path
from threads.views import (
    IndexView, ThreadDetailView, ThreadCreateView,
    ThreadUpdateView, ThreadDeleteView,
    AnswerCreateView, AnswerUpdateView, AnswerDeleteView,
)

app_name = 'threads'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('thread/create/', ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/<int:pk>/update/', ThreadUpdateView.as_view(), name='thread_update'),
    path('thread/<int:pk>/delete/', ThreadDeleteView.as_view(), name='thread_delete'),
    path('thread/<int:pk>/answer/', AnswerCreateView.as_view(), name='answer_create'),
    path('answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]
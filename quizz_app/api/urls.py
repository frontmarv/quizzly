from django.urls import path
from quizz_app.api.views import QuizzListView, QuizzDetailView

urlpatterns = [
    path('quizzes/', QuizzListView.as_view(), name='quizz-list'),
    path('quizzes/<int:pk>/', QuizzDetailView.as_view(), name='quizz-detail'),
]

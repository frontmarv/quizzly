from django.urls import path

from quizz_app.api.views import QuizView, QuizzDetailView

urlpatterns = [
    path('quizzes/', QuizView.as_view(), name='quizz-list-create'),
    path('quizzes/<int:pk>/', QuizzDetailView.as_view(), name='quizz-detail'),
]

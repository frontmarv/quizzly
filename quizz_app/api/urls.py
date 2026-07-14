from django.urls import path
from quizz_app.api.views import GenerateQuizView, QuizzDetailView

urlpatterns = [
    path('quizzes/', GenerateQuizView.as_view(), name='quizz-list-create'),
    path('quizzes/<int:pk>/', QuizzDetailView.as_view(), name='quizz-detail'),
]

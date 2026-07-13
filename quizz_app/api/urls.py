from django.urls import path

urlpatterns = [
    path('quizzes/', RegistrationView.as_view(), name='register'),
    path('quizzes/<int:pk>/', RegistrationView.as_view(), name='register')
]

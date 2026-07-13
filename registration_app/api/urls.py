from django.urls import path

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', RegistrationView.as_view(), name='register'),
    path('logout/', RegistrationView.as_view(), name='register'),
    path('token/refresh/', RegistrationView.as_view(), name='register'),
]

from django.urls import path
from .views import RegistrationView, CookieRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', RegistrationView.as_view(), name='register'),
    path('logout/', RegistrationView.as_view(), name='register'),
    path('token/refresh/', CookieRefreshView.as_view(), name='register'),
]

from django.urls import path
from .views import LoginWithGoogle
from rest_framework_simplejwt.views import TokenVerifyView
urlpatterns = [
    path('login/', LoginWithGoogle.as_view(), name='login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
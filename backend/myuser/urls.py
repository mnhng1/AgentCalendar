from django.urls import path
from .views import LoginWithGoogle

urlpatterns = [
    path('login/', LoginWithGoogle.as_view(), name='login'),
]
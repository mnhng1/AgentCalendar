from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .utils import get_id_token_with_code_method_1
from rest_framework.response import Response

def authenticate_or_create_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(username = email, email=email)
    return user


class LoginWithGoogle(APIView):
    def post(self, request):
        if 'code' in request.data.keys():
            code = request.data['code']
            id_token = get_id_token_with_code_method_1(code)
            user_email = id_token['email']
            user = authenticate_or_create_user(user_email)
            
        return Response('ok')
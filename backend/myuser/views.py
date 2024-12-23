from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import google.auth.jwt
from myuser.models import UserProfile

def authenticate_or_create_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(username = email, email=email)
    return user

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'config', 'client_secret.json')

def get_credentials_with_code(code):
    """
    Exchange authorization code for credentials.

    Parameters:
        code: str - The authorization code received from Google.

    Returns:
        credentials: Credentials object containing access and refresh tokens.
    """
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
       scopes=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/calendar'
    ],
        redirect_uri="postmessage"
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials




@method_decorator(csrf_exempt, name='dispatch')
class LoginWithGoogle(APIView):
    def post(self, request):
        if 'code' in request.data.keys():
            try:
                code = request.data['code']
                credentials = get_credentials_with_code(code)

                # Decode the ID token
                id_token = credentials.id_token
                decoded_token = google.auth.jwt.decode(id_token, verify=False)  # Decoded as a dictionary
                user_email = decoded_token.get('email')

                # Handle user authentication/creation
                user = authenticate_or_create_user(user_email)
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.refresh_token = credentials.refresh_token
                user_profile.save()

                # Generate and return JWT
                token = AccessToken.for_user(user)
                return Response({
                    'access_token': str(token),
                    'user_name': user_email
                })

            except Exception as e:
                print(f'Error during login: {e}') 
                return Response({'error': str(e)}, status=500)
        
        return Response({'error': 'Invalid request'}, status=400)
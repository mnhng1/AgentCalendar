from django.shortcuts import render
from rest_framework.views import APIView
from .agent_core.calendar_chain import CalendarAgent
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from myuser.models import UserProfile

class ExecuteAgent(APIView):
    def post(self, request):
        try:
            token_header = request.headers.get('Authorization', '')
            if not token_header.startswith('Bearer '):
                return Response({'error': 'Invalid Authorization header'}, status=401)
            token_str = token_header.split(' ')[1]

            # Decode the JWT access token to get the user
            token = AccessToken(token_str)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)

            # Retrieve UserProfile
            user_profile = UserProfile.objects.get(user=user)
            refresh_token = user_profile.refresh_token

            if not refresh_token:
                return Response({'error': 'No refresh token available'}, status=400)

            messages = request.data.get('messages', [])
            user_input = request.data.get('input', '')

            # Initialize the CalendarAgent with access_token and refresh_token
            agent = CalendarAgent(access_token=token_str, refresh_token=refresh_token)
            response = agent.run({
                "chat_history": messages,
                "input": user_input,
                "agent_scratchpad": []  # Initialize empty scratchpad
            })
            assistant_response = response.get('output', 'Sorry, I could not process your request')
            return Response(assistant_response)
        except (InvalidToken, TokenError):
            return Response({'error': 'Invalid access token'}, status=401)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



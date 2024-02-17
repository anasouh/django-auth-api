from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework import authentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import PasswordReset
from rest_framework.exceptions import ErrorDetail

class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({'error': str(e.args[0])}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class TokenVerifyAPIView(GenericAPIView):
    serializer_class = TokenVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetAPIView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(email=serializer.data['email'])
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            old_password_reset = PasswordReset.objects.filter(user=user)
            if old_password_reset.exists():
                old_password_reset.delete()
            password_reset = PasswordReset.objects.create(user=user, token=token)
            password_reset.save()
            password_reset.send_email(serializer.data['email'])
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class PasswordChangeAPIView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['new_password'])
                user.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
class PasswordResetChangeAPIView(GenericAPIView):
    serializer_class = PasswordResetChangeSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({'error': str(e.args[0]['non_field_errors'][0])}, status=status.HTTP_400_BAD_REQUEST)
        password_reset = PasswordReset.objects.get(token=serializer.data['token'])
        if password_reset.is_expired:
            password_reset.delete()
            return JsonResponse({'error': 'authentication.resetPasswordTokenExpired'}, status=status.HTTP_400_BAD_REQUEST)
        user = password_reset.user
        user.set_password(serializer.data['new_password'])
        password_reset.delete()
        user.save()
        return Response(status=status.HTTP_200_OK)
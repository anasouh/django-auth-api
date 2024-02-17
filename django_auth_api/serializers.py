from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import PasswordReset
from django.db import IntegrityError
from django.db.models import Q

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    @staticmethod
    def is_password_valid(password):
        if len(password) < 8:
            raise serializers.ValidationError('authentication.passwordTooShort')
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('authentication.passwordDigits')
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError('authentication.passwordUppercase')
        if not any(char.islower() for char in password):
            raise serializers.ValidationError('authentication.passwordLowercase')
        return True
    
    def is_username_valid(self, username):
        if len(username) < 4:
            raise serializers.ValidationError('authentication.usernameTooShort')
        return True
    
    def validate(self, attrs):
        self.is_password_valid(attrs['password'])
        self.is_username_valid(attrs['username'])
        
        if get_user_model().objects.filter(Q(username=attrs['username']) | Q(email=attrs['email'])).exists():
            raise IntegrityError('authentication.usernameOrEmailTaken')
        
        return attrs
    

    def create(self, validated_data):
        
        
        if self.is_password_valid(validated_data['password']):
            user = super(CreateUserSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
    
class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
    
    class Meta:
        fields = ('token',)

    def validate(self, attrs):
        token = attrs.get('token')
        if not token:
            raise serializers.ValidationError('Token is required')
        if not Token.objects.filter(key=token).exists():
            raise serializers.ValidationError('Token is invalid')
        return attrs
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ('email',)
    
    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError('Email is required')
        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is invalid')
        return attrs
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    
    class Meta:
        fields = ('old_password', 'new_password',)
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if not old_password:
            raise serializers.ValidationError('Old password is required')
        if not new_password:
            raise serializers.ValidationError('New password is required')
        return attrs
    
class PasswordResetChangeSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()
    
    class Meta:
        fields = ('token', 'new_password',)
    
    def validate(self, attrs):
        token = attrs.get('token')
        new_password = attrs.get('new_password')
        if not token:
            raise serializers.ValidationError('errors.post')
        if not new_password:
            raise serializers.ValidationError('New password is required')
        if not PasswordReset.objects.filter(token=token).exists():
            raise serializers.ValidationError('errors.unauthorized')
        CreateUserSerializer.is_password_valid(new_password)
        return attrs
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from django.urls import re_path


urlpatterns = [
    re_path(r'^auth/login/$',
        obtain_auth_token,
        name='auth_user_login'),
    re_path(r'^auth/signup/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    re_path(r'^auth/logout/$',
        LogoutUserAPIView.as_view(),
        name='auth_user_logout'),
    re_path(r'^auth/token/verify/$',
        TokenVerifyAPIView.as_view(),
        name='auth_user_token_verify'),
    re_path(r'^auth/password/reset/$',
        PasswordResetAPIView.as_view(),
        name='auth_user_password_reset'),
    re_path(r'^auth/password/reset/change/$',
        PasswordResetChangeAPIView.as_view(),
        name='auth_user_password_reset_change'),
    re_path(r'^auth/password/change/$',
        PasswordChangeAPIView.as_view(),
        name='auth_user_password_change'),
]
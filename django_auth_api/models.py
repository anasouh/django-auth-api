from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta, timezone

class PasswordReset(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return datetime.now(timezone.utc) > self.created_at + timedelta(minutes=30)

    def send_email(self, email):
        subject = "Password Reset"
        html_message = render_to_string('email/password_reset.html', {
            'user': self.user,
            'name': settings.DISPLAYED_NAME,
            'password_reset_url': settings.PASSWORD_RESET_URL,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': PasswordResetTokenGenerator().make_token(self.user),
        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = email
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
    def __str__(self):
        return self.user.email + " - " + self.token
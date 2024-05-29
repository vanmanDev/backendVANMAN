from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True , unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_superuser = models.BooleanField(_('staff'), default=False)
    role = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_logged_in = models.BooleanField(_('logged in'), default=False)
    is_activated = models.BooleanField(_('activated'), default=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # the below like concatinates your websites reset password url and the reset email token which will be required at a later stage
    email_html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Password Reset for Crediation portal account</title>
            <style>
                /* Inline CSS styles */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    color: #555;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    text-decoration: none;
                    color:white;
                    border-radius: 5px;
                    border: none;
                    cursor: pointer;
                }}
                .button:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Password Reset</h1>
                <p>Dear user,</p>
                <p>We received a request to reset your password for the Crediation portal account. If you did not make this request, please ignore this email.</p>
                <p>To reset your password, please click the button below:</p>
                <a href="{instance.request.build_absolute_uri('https://vanman.vercel.app/reset-password/')}{reset_password_token.key}" class="button">Reset Password</a>
                <p>If the button above doesn't work, you can copy and paste the following URL into your browser's address bar:</p>
                <p>{instance.request.build_absolute_uri('https://vanman.vercel.app/reset-password/')}{reset_password_token.key}</p>
                <p>Thank you.</p>
                <p>Best regards,<br>VANMAN Company</p>
            </div>
        </body>
        </html>
    """
    send_mail(
        # title:
        # Subject
        "You requested for reset password.",
        # Message (HTML content)
        "",
        # Sender
        "VANMAN Company",
        # Recipient
        [reset_password_token.user.email],
        # HTML message
        html_message=email_html_message,
        # Do not fail silently (raise an exception if sending fails)
        fail_silently=False,
    )

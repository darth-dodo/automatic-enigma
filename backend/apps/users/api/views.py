from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import random
from django.conf import settings

User = get_user_model()

def send_otp_via_twilio(phone, otp):
    if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_FROM_NUMBER:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_FROM_NUMBER,
            to=phone
        )
        return message.sid
    return None

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user.failed_login_attempts = 0
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            try:
                user = User.objects.get(username=username)
                user.failed_login_attempts += 1
                user.save()
                if user.failed_login_attempts >= 3:
                    return Response({'detail': 'Too many failed attempts. Use password reset.'},
                                    status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                pass
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class RequestOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone)
            otp = f"{random.randint(100000, 999999)}"
            user.otp_code = otp
            user.otp_expiry = timezone.now() + timedelta(minutes=5)
            user.save()
            send_otp_via_twilio(phone, otp)
            return Response({'detail': 'OTP sent.'})
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone_number')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(phone_number=phone)
            if user.otp_code == otp and user.otp_expiry > timezone.now():
                refresh = RefreshToken.for_user(user)
                user.otp_code = None
                user.otp_expiry = None
                user.failed_login_attempts = 0
                user.save()
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(username=username)
            if user.failed_login_attempts >= 3:
                user.set_password(new_password)
                user.failed_login_attempts = 0
                user.save()
                return Response({'detail': 'Password reset successful.'})
            return Response({'detail': 'Password reset not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

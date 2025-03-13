from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from .models import OTP
from .serializers import OTPSerializer

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        expiration_time = timezone.now() + timedelta(minutes=5)

        # Store OTP in the database
        otp_instance, created = OTP.objects.update_or_create(
            email=email,
            defaults={'otp': otp, 'expiration_time': expiration_time}
        )

        # Send OTP via email
        try:
            send_mail(
                'Your OTP for SmartInvestApp',
                f'Your OTP is {otp}. It will expire in 5 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = OTP.objects.get(email=email)
            if otp_instance.otp != otp:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            if timezone.now() > otp_instance.expiration_time:
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

            # OTP is valid, delete it from the database
            otp_instance.delete()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        except OTP.DoesNotExist:
            return Response({'error': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)
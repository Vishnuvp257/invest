from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser

@api_view(['POST'])
def register(request):
    """User registration API"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)  # Create a token for new user
        return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """User login API"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)  # Get or create a token for the user
        return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """User logout API"""
    try:
        request.auth.delete()  # Delete the token on logout
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except AttributeError:
        return Response({"error": "Invalid token or already logged out"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """Fetch authenticated user details"""
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dob": user.dob,
        "native": user.native,
        "gender": user.gender,
        "type": user.type  # ✅ Ensure 'type' is included in the response
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_type(request):
    """Update the user's investment type after answering the question."""
    user = request.user
    new_type = request.data.get('type')

    if new_type not in ['Beginner', 'Intermediate', 'Expert']:
        return Response({"error": "Invalid type selected"}, status=status.HTTP_400_BAD_REQUEST)

    user.type = new_type
    user.save()

    # ✅ Debugging log
    updated_user = CustomUser.objects.get(id=user.id)
    print(f"✅ Updated User: {updated_user.username}, Type: {updated_user.type}")  

    return Response({"message": "User type updated successfully", "type": updated_user.type}, status=status.HTTP_200_OK)

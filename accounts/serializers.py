from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'dob', 'native', 'gender', 'type']
        extra_kwargs = {'type': {'read_only': True}}  # Type should be updated via a separate API

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dob=validated_data['dob'],
            native=validated_data['native'],
            gender=validated_data['gender'],
        )
        return user

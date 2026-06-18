from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
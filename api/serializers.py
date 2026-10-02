from .models import Analysis
from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
      
        
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        
    
    def create(self, validated_data):
        """Создаем пользователя с хэшированным паролем."""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', User.Role.CLIENT)
        )
        
        return user
        
        
class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'user', 'date', 'title', 'data', 'created_at']
        read_only_fields = ['user', 'created_at']
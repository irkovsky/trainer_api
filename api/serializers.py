from .models import Analysis, Workout, ExerciseSet, Exercise
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
      
        
class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = [
            'id', 'exercise', 'user', 'set_number',
            'reps', 'weight',
            'rpe', 'note',
            'completed_at'
        ]
        read_only_fields = ['user', 'completed_at']
        
    
class ExerciseSerializer(serializers.ModelSerializer):
     sets = ExerciseSetSerializer(many=True, read_only=True)
     
     class Meta:
         model = Exercise
         fields = [
             'id', 'workout', 
             'name', 'order',
             'planned_sets', 'planned_reps', 'planned_weight',
             'sets'
         ]
         
         
class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Workout
        fields = [
            'id', 'user', 'title', 'description' , 
            'date', 'created_at', 'exercises'
        ]
        read_only_fields = ['created_at']
        
        
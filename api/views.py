from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .serializers import (
    RegisterSerializer, AnalysisSerializer, WorkoutSerializer,
    ExerciseSerializer, ExerciseSetSerializer
)
from .models import Analysis, Workout, Exercise, ExerciseSet
from .filters import AnalysisFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import AnalysisPagination, WorkoutPagination

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsAdmin

from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all().order_by('-created_at')
    serializer_class = AnalysisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnalysisFilter
    pagination_class = AnalysisPagination
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if user.role == 'admin':
            return queryset.all()
        return queryset.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    pagination_class = WorkoutPagination
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset.none()
        
        if user.role == 'admin':
            return queryset.all()
        
        return queryset.filter(user=user)
    
    
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Exercise.objects.all()
        return Exercise.objects.filter(workout__user=user)


class ExerciseSetViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSet.objects.all()
    serializer_class = ExerciseSetSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ExerciseSet.objects.all()
        return ExerciseSet.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        

            
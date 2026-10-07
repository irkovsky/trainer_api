from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import RegisterView, AnalysisViewSet, WorkoutViewSet


router = DefaultRouter()
router.register(r'analyses', AnalysisViewSet, basename='analysis')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
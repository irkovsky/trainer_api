from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import RegisterView, AnalysisViewSet


router = DefaultRouter()
router.register(r'analyses', AnalysisViewSet, basename='analysis')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
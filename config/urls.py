"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views_web

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),    
    
    # ============================================================
    # AUTH (WEB)
    # ============================================================
    path('register', views_web.register, name='register'),
    path('login', views_web.UserLoginView.as_view(), name='login'),
    path('logout', views_web.UserLogoutView.as_view(), name='logout'),
    
    # ============================================================
    # ANALYSIS (WEB)
    # ============================================================
    path('analyses/', views_web.analysis_list, name='analysis_list'),
    path('analyses/create/', views_web.analysis_create, name='analysis_create'),
    path('analyses/<int:pk>/', views_web.analysis_detail, name='analysis_detail'),
    path('analyses/<int:pk>/update/', views_web.analysis_update, name='analysis_update'),
    path('analyses/<int:pk>/delete/', views_web.analysis_delete, name='analysis_delete'),
    
    # ============================================================
    # WORKOUT (WEB)
    # ============================================================
    path('workouts/', views_web.workout_list, name='workout_list'),
    path('workouts/create/', views_web.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views_web.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/update/', views_web.workout_update, name='workout_update'),
    path('workouts/<int:pk>/delete/', views_web.workout_delete, name='workout_delete'),
    
    # ============================================================
    # EXERCISE (WEB)
    # ============================================================
    path(
        'workouts/<int:workout_pk>/exercise/create/',
        views_web.exercise_create,
        name='exercise_create'
    ),
    path(
        'exercises/<int:pk>/update',
        views_web.exercise_update,
        name='exercise_update'
    ),
    path(
        'exercises/<int:pk>/delete',
        views_web.exercise_delete,
        name='exercise_delete'
    ),
    
    # ============================================================
    # EXERCISE SET (WEB)
    # ============================================================
    path(
        'exercises/<int:exercise_pk>/sets/create/',
        views_web.exercise_set_create,
        name='exercise_set_create'
    ),
    path(
        'exercise-sets/<int:pk>/delete/',
        views_web.exercise_set_delete,
        name='exercise_set_delete'
    ) 
]

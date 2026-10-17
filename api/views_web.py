from .models import Analysis, Workout, Exercise, ExerciseSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import (
    AnalysisForm, RegisterForm, WorkoutForm, 
    ExerciseForm, ExerciseSetForm
)
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied

@login_required
def analysis_list(request):
    if request.user.role == 'admin':
        analyses = Analysis.objects.all()
    else:
        analyses = Analysis.objects.filter(user=request.user)
    return render(request, 'analyses/analysis_list.html', {'analyses': analyses})

@login_required
def analysis_create(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            return redirect('analysis_list')
        
    else: 
        form = AnalysisForm()
    return render(request, 'analyses/analysis_form.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('analysis_list')
    
    
class UserLogoutView(LogoutView):
    next_page = 'login'
    

@login_required    
def analysis_detail(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
        return redirect('analysis_list')
    
    return render(request, 'analyses/analysis_detail.html', {'analysis': analysis})


@login_required
def analysis_update(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
        return redirect('analysis_list')
    
    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('analysis_detail', pk=analysis.pk)
    else:
        form = AnalysisForm(instance=analysis)
        
    return render(request, 'analyses/analysis_form.html', {'form': form})

@login_required
def analysis_delete(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
            return redirect('analysis_list') 
    
    if request.method == 'POST':
        analysis.delete()
        return redirect('analysis_list')
    else:
        return render(request, 'analyses/analysis_confirm_delete.html', {'analysis': analysis})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('analysis_list')
    else:    
        form = RegisterForm()
        
    return render(request, 'auth/register.html', {'form': form})


def workout_list(request):
    if request.user.role == 'admin':
        workouts = Workout.objects.all()
    else:
        workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    
    if request.user.role != 'admin' and request.user != workout.user:
        return redirect('workout_list')
    
    exercises = workout.exercises.all()
    return render(request, 'workouts/workout_detail.html', {
        'workout': workout,
        'exercises': exercises
    })

def workout_create(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    
    if request.method == 'POST':    
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'workouts/workout_form.html', {'form': form})
    

def workout_update(request, pk):
    if request.user.role != 'admin':
        raise PermissionDenied
    
    workout = get_object_or_404(Workout, pk=pk)
    
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workout_detail', pk=workout.id)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'workouts/workout_form.html', {'form': form})

def workout_delete(request, pk):
    if request.user.role != 'admin':
            raise PermissionDenied
    
    workout = get_object_or_404(Workout, pk=pk)
    
    if request.method == 'POST':
        workout.delete()
        return redirect('workout_list')
    
    return render(request, 'workouts/workout_confirm_delete.html', {'workout': workout})


# ============================================================================
# УПРАЖНЕНИЯ
# ============================================================================

@login_required
def exercise_create(request, workout_pk):
    if request.user.role != 'admin':
        raise PermissionDenied
    
    workout = get_object_or_404(Workout, pk=workout_pk)
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            return redirect('workout_detail', pk=workout_pk)
    
    form = ExerciseForm()
    return render(request, 'workouts/exercise_form.html', {
        'form': form,
        'workout': workout,
    })
    
@login_required
def exercise_update(request, pk):
    if request.user.role != 'admin':
        raise PermissionDenied
    
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('workout_detail', pk=exercise.workout.pk)
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'workouts/exercise_form.html', {
        'form': form,
        'workout': exercise.workout,
    })
    
    
@login_required  
def exercise_delete(request, pk):
    if request.user.role != 'admin':
        raise PermissionDenied
        
    exercise = get_object_or_404(Exercise, pk=pk)
    workout_pk = exercise.workout.pk
    
    if request.method == 'POST':
        exercise.delete()
        return redirect('workout_detail', pk=workout_pk)
    return render(request, 'workouts/exercise_confirm_delete.html', {'exercise': exercise})


@login_required
def exercise_set_create(request, exercise_pk):
    exercise = get_object_or_404(Exercise, pk=exercise_pk)
    
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST)
        if form.is_valid():
            exercise_set = form.save(commit=False)
            exercise_set.exercise = exercise
            exercise_set.user = request.user
            exercise_set.save()
            return redirect('workout_detail', exercise.workout.pk)
    else:
        form = ExerciseSetForm()
    return render(request, 'workouts/exerciseset_form.html', {
        'form': form,
        'exercise': exercise,
    }) 
    
@login_required  
def exercise_set_delete(request, pk):
    exercise_set = get_object_or_404(ExerciseSet, pk=pk)
    if request.user.role != 'admin' and exercise_set.user != request.user:
        raise PermissionDenied
    
    workout_pk = exercise_set.exercise.workout.pk
    if request.method == 'POST':
        exercise_set.delete()
        return redirect('workout_detail', workout_pk)
        
    return render(request, 'workouts/exerciseset_confirm_delete.html', {
        'exercises_set': exercise_set
    })
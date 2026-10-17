from .models import Analysis, Workout, ExerciseSet, Exercise
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['date', 'title', 'data']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
        
        
class RegisterForm(UserCreationForm):
    # password = None
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
        
        
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['user', 'title', 'description', 'date']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
        
        
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'order', 'planned_sets', 'planned_reps', 'planned_weight']
        
class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['set_number', 'reps', 'weight', 'rpe', 'note']
        

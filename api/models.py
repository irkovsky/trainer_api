from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        ADMIN = 'admin', 'Администратор'
    
    role = models.CharField(
        max_length=10, 
        choices=Role, 
        default=Role.CLIENT
    )
    
    
class Analysis(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='analyses'
    )
    
    date = models.DateField()
    title = models.CharField(max_length=200)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} {self.date}'
    
    
class Workout(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f'{self.title} {self.date}'
    

class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    planned_sets = models.PositiveIntegerField(default=3)
    planned_reps = models.PositiveIntegerField(default=10)
    planned_weight = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['workout', 'order']
    
    def __str__(self):
        return f"{self.name} ({self.planned_sets}x{self.planned_reps})"
    
    
class ExerciseSet(models.Model):
    class RPEChoices(models.IntegerChoices):
        VERY_EASY = 1, 'Очень легко'
        EASY = 2, 'Легко'
        MODERATE_EASY = 3, 'Умеренно легко' 
        MODERATE = 4, 'Средне'
        MODERATE_HARD = 5, 'Умеренно тяжело' 
        HARD = 6, 'Тяжело'
        VERY_HARD = 7, 'Очень тяжело'
        EXTREME = 8, 'Экстремально'   
        MAXIMUM = 9, 'Максимум'
        FAILURE = 10, 'Отказ'
            
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name = 'sets'    
        )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='exercise_sets'
    )
    set_number = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField()
    weight = models.FloatField(null=True, blank=True)
    
    rpe = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=RPEChoices.choices
    )
    
    note = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['exercise', 'user', 'set_number']
        unique_together = ('exercise', 'user', 'set_number')
        
    def __str__(self):
        return f'{self.exercise.name} - {self.reps}x{self.weight}'

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
    

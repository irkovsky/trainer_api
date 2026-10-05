from .models import Analysis
from django import forms


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
        

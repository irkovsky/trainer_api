import django_filters
from .models import Analysis

class AnalysisFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Analysis
        fields = ['date', 'title']
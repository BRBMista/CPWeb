import django_filters
from .models import Student

class StudentFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Фамилия')
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='Имя')
    group = django_filters.CharFilter(lookup_expr='icontains', label='Группа')

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group']
import django_filters
from .models import Book, Course

class BookFilter(django_filters.FilterSet):
    course = django_filters.ModelChoiceFilter(field_name='course', lookup_expr='exact', label='Course', distinct=True, queryset=Course.objects.all())
    course_subj = django_filters.CharFilter(field_name='course__subject', lookup_expr='iexact', label='Course Subject', distinct=True)
    course_cn = django_filters.CharFilter(field_name='course__class_number', lookup_expr='exact', label='Course Number', distinct=True)
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title', distinct=True)
    seller = django_filters.CharFilter(field_name='seller__username', lookup_expr='icontains', label='Seller', distinct=True)
    class Meta:
        model = Book
        fields = ['course', 'course_subj', 'course_cn', 'title', 'seller']
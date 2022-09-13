from django_filters import rest_framework as filters

from works.models import Work

class WorkFilter(filters.FilterSet):
    area = filters.CharFilter(field_name="knowledge_area", lookup_expr="icontains")
    visibility = filters.CharFilter(lookup_expr="icontains")
    is_reviewed = filters.BooleanFilter()

   
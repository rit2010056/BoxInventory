from .models import Box
import django_filters

class BoxFilters(django_filters.FilterSet):
    length_more_than = django_filters.NumberFilter(field_name="length", lookup_expr='gt')
    length_less_than = django_filters.NumberFilter(field_name="length", lookup_expr='lt')

    breadth_more_than = django_filters.NumberFilter(field_name="width", lookup_expr='gt')
    breadth_less_than = django_filters.NumberFilter(field_name="width", lookup_expr='lt')

    height_more_than = django_filters.NumberFilter(field_name="height", lookup_expr='gt')
    height_less_than = django_filters.NumberFilter(field_name="height", lookup_expr='lt')

    area_more_than = django_filters.NumberFilter(field_name="area", lookup_expr='gt')
    area_less_than = django_filters.NumberFilter(field_name="area", lookup_expr='lt')

    volume_more_than = django_filters.NumberFilter(field_name="volume", lookup_expr='gt')
    volume_less_than = django_filters.NumberFilter(field_name="volume", lookup_expr='lt')

    create_after = django_filters.NumberFilter(field_name="created_at", lookup_expr='gt')
    create_before = django_filters.NumberFilter(field_name="created_at", lookup_expr='lt')

    created_by = django_filters.CharFilter(method="created_by_filter",)


    class Meta:
        model = Box
        fields = ['length', "width", "height", "volume", "area", "created_at", "created_by"]

    def created_by_filter(self, queryset, name, value):
        return queryset.filter(created_by__username=value)



class BoxUserFilters(django_filters.FilterSet):
    length_more_than = django_filters.NumberFilter(field_name="length", lookup_expr='gt')
    length_less_than = django_filters.NumberFilter(field_name="length", lookup_expr='lt')

    breadth_more_than = django_filters.NumberFilter(field_name="width", lookup_expr='gt')
    breadth_less_than = django_filters.NumberFilter(field_name="width", lookup_expr='lt')

    height_more_than = django_filters.NumberFilter(field_name="height", lookup_expr='gt')
    height_less_than = django_filters.NumberFilter(field_name="height", lookup_expr='lt')

    area_more_than = django_filters.NumberFilter(field_name="area", lookup_expr='gt')
    area_less_than = django_filters.NumberFilter(field_name="area", lookup_expr='lt')

    volume_more_than = django_filters.NumberFilter(field_name="volume", lookup_expr='gt')
    volume_less_than = django_filters.NumberFilter(field_name="volume", lookup_expr='lt')

    class Meta:
        model = Box
        fields = ['length', "width", "height", "volume", "area"]
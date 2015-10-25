import django_filters

import apps.orders.models as models


class OrderFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name="total_price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="total_price", lookup_type='lte')
    start_date = django_filters.DateFilter(name='date',lookup_type=('lt'),)
    end_date = django_filters.DateFilter(name='date',lookup_type=('gt'))

    class Meta:
        model = models.Order
        fields = ['lengow_status', 'marketplace_status',
                  'min_price', 'max_price',
                  'start_date', 'end_date', 'marketplace__name']
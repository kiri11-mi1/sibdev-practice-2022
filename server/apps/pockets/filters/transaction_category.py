from django_filters import rest_framework as filters
from ..models import TransactionCategory, Transaction


class TransactionCategoryFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name='transactions__transaction_date__month')
    year = filters.NumberFilter(field_name='transactions__transaction_date__year')

    class Meta:
        model = TransactionCategory
        fields = ('month', 'year')

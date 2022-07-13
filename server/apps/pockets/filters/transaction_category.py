from django_filters import rest_framework as filters
from ..models import TransactionCategory


class TransactionCategoryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='transactions__transaction_date')

    class Meta:
        model = TransactionCategory
        fields = ['date']

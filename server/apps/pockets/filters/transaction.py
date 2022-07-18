from django_filters import rest_framework as filters, OrderingFilter

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='transaction_date__year')
    month = filters.NumberFilter(field_name='transaction_date__month')

    ordering = OrderingFilter(
        fields=(
            ('transaction_date', 'date'),
            ('amount', 'amount'),
            ('category__name', 'category'),
        )
    )

    class Meta:
        model = Transaction
        fields = ('ordering', 'year', 'month')

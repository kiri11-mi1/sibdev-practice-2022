from decimal import Decimal
from typing import Type, Union

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionFilter
from ..models import Transaction
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
    TransactionGlobalSerializer,
    TransactionBalanceSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == 'total':
            serializer_class = TransactionGlobalSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            serializer_class = TransactionCreateSerializer
        elif self.action == 'balance':
            serializer_class = TransactionBalanceSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:
        queryset = Transaction.objects.filter(
            user=self.request.user,
        ).select_related(
            'category',
        ).order_by(
            '-transaction_date', '-id',
        )

        return queryset

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        if self.action == 'total':
            obj = self.filter_queryset(self.get_queryset()).aggregate_totals()
        elif self.action == 'balance':
            obj = self.filter_queryset(self.get_queryset()).aggregate_balance()
        else:
            obj = super().get_object()

        return obj

    @action(methods=('GET',), detail=False, url_path='global')
    def total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='balance')
    def balance(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

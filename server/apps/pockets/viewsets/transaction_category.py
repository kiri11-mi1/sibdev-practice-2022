from typing import Type

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionCategoryFilter
from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategoryTransactionSumSerializer,
    TopCategoriesSerializer,
)
from ..constants import TOP_CATEGORIES


class TransactionCategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionCategoryFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        serializer_class = TransactionCategorySerializer
        if self.action == 'expenses':
            serializer_class = TransactionCategoryTransactionSumSerializer
        if self.action == 'top':
            serializer_class = TopCategoriesSerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).annotate_with_transaction_sums().order_by(
            '-transactions_sum',
        )

        return queryset

    def get_object(self):
        if self.action == 'top':
            queryset = self.get_queryset().aggregate_top_categories()
            return self.get_serializer(queryset, many=True).data
        else:
            return super().get_object()

    @action(methods=('GET',), detail=False, url_path='expenses-by-categories')
    def expenses(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='top-three-categories')
    def top(self, request: Request) -> Response:
        return Response(self.get_object(), status=status.HTTP_200_OK)

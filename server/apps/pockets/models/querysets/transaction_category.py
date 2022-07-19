from django.db.models import QuerySet, Sum, DecimalField
from django.db.models.functions import Coalesce

from apps.pockets.constants import TOP_CATEGORIES


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            transactions_sum=Coalesce(
                Sum('transactions__amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def aggregate_top_categories(self):
        top_categories = list(self[:TOP_CATEGORIES].values())
        top_categories.append(
            {
                'name': 'Другое',
                'transactions_sum': self[TOP_CATEGORIES:].aggregate(
                    Sum('transactions_sum')
                )['transactions_sum__sum']
            }
        )
        return top_categories

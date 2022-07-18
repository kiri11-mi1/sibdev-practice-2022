from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .managers import TransactionManager
from ..constants import TransactionTypes


class Transaction(models.Model):
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionTypes.CHOICES,
        verbose_name='Тип операции',
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Категория',
        null=True,
        default=None,
    )
    transaction_date = models.DateField(
        verbose_name='Дата операции',
        auto_now_add=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма операции',
        validators=(MinValueValidator(Decimal('0.01')),),
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self) -> str:
        return f'{self.amount} {TransactionTypes.CHOICES_DICT[self.transaction_type]}'

